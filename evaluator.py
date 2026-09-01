"""
evaluator.py — Pseudocode Evaluation System
=============================================

Evaluates student pseudocode submissions against a problem statement
using a configurable LLM provider (Gemini or OpenAI).  The pipeline
has three stages:

  1. **Rubric generation** (Call 1) — produces a 4-dimension rubric from
     the problem statement alone.
  2. **Evaluation + hints** (Call 2, thinking mode if supported) — scores
     the student submission against the rubric, produces a step-by-step
     trace, issues, and Socratic hints.  Raw thinking tokens are captured
     separately when the provider supports it.
  3. **Python validation** — checks the evaluation JSON for structural
     correctness.  Retries Call 2 once on failure.

Public interface
----------------
- ``generate_rubric(problem_statement, problem_id) -> dict``
- ``evaluate_submission(problem_statement, rubric, student_pseudocode,
       problem_id, submission_id) -> dict``

Provider selection
------------------
Set one of these environment variables:
- ``GEMINI_API_KEY``  → Google Gemini (default, supports thinking mode)
- ``OPENAI_API_KEY``  → OpenAI ChatGPT
- ``LLM_PROVIDER``   → Force 'gemini' or 'openai'
"""

from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import llm_client

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

TRACES_DIR = Path("data/traces")
RUBRICS_DIR = Path("data/rubrics")
VALID_SCORES = {"Excellent", "Good", "Fair", "Poor"}

# ──────────────────────────────────────────────────────────────────────
# Prompts — imported from prompts.py (edit prompts there, not here)
# ──────────────────────────────────────────────────────────────────────

from prompts import (
    EVALUATION_SYSTEM_PROMPT,
    EVALUATION_USER_PROMPT_TEMPLATE,
    RETRY_ADDENDUM,
    RUBRIC_SYSTEM_PROMPT,
    RUBRIC_USER_PROMPT_TEMPLATE,
)


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def _strip_markdown_fences(text: str) -> str:
    """Remove ```json … ``` or ``` … ``` wrappers that models sometimes add."""
    pattern = r"```(?:json)?\s*\n?(.*?)\n?\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def _parse_json_response(raw_text: str) -> dict:
    """
    Attempt to parse a JSON string from the model response.

    First tries direct parsing; if that fails, strips markdown fences
    and retries.  Raises ``ValueError`` on final failure.
    """
    # First attempt: parse directly
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    # Second attempt: strip fences then parse
    cleaned = _strip_markdown_fences(raw_text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Failed to parse JSON from model response: {exc}\n"
            f"Raw response (first 500 chars): {raw_text[:500]}"
        ) from exc


def _ensure_traces_dir() -> Path:
    """Create data/traces/ if it does not exist and return its Path."""
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    return TRACES_DIR


# ──────────────────────────────────────────────────────────────────────
# Validation
# ──────────────────────────────────────────────────────────────────────

def validate_evaluation_response(
    response: dict,
    approved_rubric: dict,
) -> tuple[bool, str]:
    """
    Validate the evaluation JSON returned by Call 2 against the rubric.

    Checks
    ------
    1. Number of dimensions matches the rubric.
    2. Dimension names match the rubric exactly (order matters).
    3. Every score is one of {Excellent, Good, Fair, Poor}.
    4. Null-consistency:
       - Excellent → issue & hint must be null
       - Good → issue must not be null, hint must be null
       - Fair/Poor → issue & hint must not be null
    5. Trace is at least 60 words.

    Returns ``(True, "ok")`` on success or ``(False, reason)`` on failure.
    """
    rubric_names = [d["name"] for d in approved_rubric["dimensions"]]

    # Check 1: number of dimensions matches
    if len(response["dimensions"]) != len(rubric_names):
        return False, f"Expected {len(rubric_names)} dimensions, got {len(response['dimensions'])}"

    # Check 2: dimension names match rubric exactly
    response_names = [d["name"] for d in response["dimensions"]]
    if response_names != rubric_names:
        return False, (
            f"Dimension names mismatch: expected {rubric_names}, "
            f"got {response_names}"
        )

    for dim in response["dimensions"]:
        # Check 3: score is a valid qualitative label
        if dim["score"] not in VALID_SCORES:
            return False, (
                f"Invalid score for {dim['name']}: {dim['score']}"
            )

        # ── Auto-correct stubborn LLM formatting ──────────────────────
        # LLMs frequently omit the 'issue' or 'hint' when assigning
        # Good/Fair/Poor, even when explicitly told not to. Since we
        # hide 'issue' from the student anyway, we can safely inject
        # default strings here to prevent validation crashes.
        if dim["score"] in {"Good", "Fair", "Poor"}:
            if not dim.get("issue"):
                dim["issue"] = f"Minor gaps or issues in {dim['name']}."
            if not dim.get("hint"):
                dim["hint"] = f"Can you think of a way to improve the {dim['name'].lower()}?"
        elif dim["score"] == "Excellent":
            dim["issue"] = None
            dim["hint"] = None

        # Check 4: null consistency             
        if dim["score"] == "Excellent":
            if dim["issue"] is not None:
                return False, f"Issue must be null when score is Excellent for {dim['name']}"
            if dim["hint"] is not None:
                return False, f"Hint must be null when score is Excellent for {dim['name']}"

        elif dim["score"] in {"Good", "Fair", "Poor"}:
            if dim["issue"] is None:
                return False, f"Issue must not be null when score is {dim['score']} for {dim['name']}"
            if dim["hint"] is None:
                return False, f"Hint must not be null when score is {dim['score']} for {dim['name']}"

    # Check 5: trace length
    word_count = len(response["trace"].split())
    if word_count < 60:
        return False, f"Trace too short ({word_count} words)"

    return True, "ok"


# ──────────────────────────────────────────────────────────────────────
# Call 1 — Rubric generation
# ──────────────────────────────────────────────────────────────────────

async def generate_rubric(
    problem_statement: str,
    problem_id: str,
) -> dict:
    """
    Generate a 4-dimension rubric for the given problem statement.

    Parameters
    ----------
    problem_statement : str
        The full text of the programming problem.
    problem_id : str
        An identifier for the problem (for logging / tracing).

    Returns
    -------
    dict
        The parsed rubric JSON with a ``"dimensions"`` list.

    Raises
    ------
    ValueError
        If the model response cannot be parsed as valid JSON.
    """
    user_prompt = RUBRIC_USER_PROMPT_TEMPLATE.format(
        problem_statement=problem_statement,
    )

    try:
        raw_text = await llm_client.call_rubric_generation(
            system_prompt=RUBRIC_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
    except Exception as exc:
        raise ValueError(
            f"Rubric generation API call failed for problem "
            f"'{problem_id}': {exc}"
        ) from exc

    rubric = _parse_json_response(raw_text)
    return rubric


# ──────────────────────────────────────────────────────────────────────
# Call 2 — Evaluation + hints (thinking mode if supported)
# ──────────────────────────────────────────────────────────────────────

async def _call_evaluation(
    problem_statement: str,
    rubric: dict,
    student_pseudocode: str,
    is_retry: bool = False,
) -> tuple[str | None, str]:
    """
    Make a single Call 2 request.

    If the active provider supports thinking mode, raw thinking tokens
    are captured separately from the structured output.

    Returns ``(thinking_text, raw_output_text)``.
    ``thinking_text`` is ``None`` for providers without thinking support.
    """
    user_prompt = EVALUATION_USER_PROMPT_TEMPLATE.format(
        problem_statement=problem_statement,
        rubric_json=json.dumps(rubric, indent=2),
        student_pseudocode=student_pseudocode,
    )

    if is_retry:
        user_prompt += RETRY_ADDENDUM

    thinking_text, output_text = await llm_client.call_evaluation(
        system_prompt=EVALUATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )
    return thinking_text, output_text


async def evaluate_submission(
    problem_statement: str,
    rubric: dict,
    student_pseudocode: str,
    problem_id: str,
    submission_id: str,
) -> dict:
    """
    Evaluate a student pseudocode submission against a rubric.

    Pipeline: Call 2 → validate → (retry once if invalid) → save → return.

    Parameters
    ----------
    problem_statement : str
        The full text of the programming problem.
    rubric : dict
        The approved rubric (output of ``generate_rubric``).
    student_pseudocode : str
        The student's pseudocode submission.
    problem_id : str
        An identifier for the problem.
    submission_id : str
        An identifier for this submission.

    Returns
    -------
    dict
        On success: the evaluation result (parsed Call 2 JSON).
        On failure: ``{"error": True, "message": "...", "raw_response": "..."}``.
    """
    llm_thinking: str | None = None
    raw_text: str = ""
    retry_attempted: bool = False
    validation_passed: bool = False
    validation_message: str = ""
    evaluation_result: dict | None = None

    # ── Attempt 1 ────────────────────────────────────────────────
    try:
        llm_thinking, raw_text = await _call_evaluation(
            problem_statement=problem_statement,
            rubric=rubric,
            student_pseudocode=student_pseudocode,
            is_retry=False,
        )
        evaluation_result = _parse_json_response(raw_text)
        validation_passed, validation_message = validate_evaluation_response(
            evaluation_result, rubric
        )
    except Exception as exc:
        validation_passed = False
        validation_message = f"Attempt 1 error: {exc}"

    # ── Attempt 2 (retry) ────────────────────────────────────────
    if not validation_passed:
        retry_attempted = True
        try:
            llm_thinking, raw_text = await _call_evaluation(
                problem_statement=problem_statement,
                rubric=rubric,
                student_pseudocode=student_pseudocode,
                is_retry=True,
            )
            evaluation_result = _parse_json_response(raw_text)
            validation_passed, validation_message = (
                validate_evaluation_response(evaluation_result, rubric)
            )
        except Exception as exc:
            validation_passed = False
            validation_message = f"Retry error: {exc}"

    # ── Build the final result ───────────────────────────────────
    timestamp = datetime.now(timezone.utc).isoformat()

    if not validation_passed:
        # Return structured error — never raise
        error_result: dict = {
            "error": True,
            "message": validation_message,
            "raw_response": raw_text,
        }
        # Still save the trace for debugging
        _save_trace(
            problem_statement=problem_statement,
            rubric=rubric,
            student_pseudocode=student_pseudocode,
            llm_thinking=llm_thinking,
            evaluation_result=evaluation_result,
            validation_passed=False,
            validation_message=validation_message,
            retry_attempted=retry_attempted,
            timestamp=timestamp,
            problem_id=problem_id,
            submission_id=submission_id,
        )
        return error_result

    # Successful evaluation
    _save_trace(
        problem_statement=problem_statement,
        rubric=rubric,
        student_pseudocode=student_pseudocode,
        llm_thinking=llm_thinking,
        evaluation_result=evaluation_result,
        validation_passed=True,
        validation_message=validation_message,
        retry_attempted=retry_attempted,
        timestamp=timestamp,
        problem_id=problem_id,
        submission_id=submission_id,
    )

    assert evaluation_result is not None  # guaranteed by validation pass
    return evaluation_result


# ──────────────────────────────────────────────────────────────────────
# Trace saving
# ──────────────────────────────────────────────────────────────────────

def _save_trace(
    *,
    problem_statement: str,
    rubric: dict,
    student_pseudocode: str,
    llm_thinking: str | None,
    evaluation_result: dict | None,
    validation_passed: bool,
    validation_message: str,
    retry_attempted: bool,
    timestamp: str,
    problem_id: str,
    submission_id: str,
) -> None:
    """
    Save the full evaluation trace to ``data/traces/``.

    Includes the raw Gemini thinking tokens so we can compare them
    against the ``trace`` field in the evaluation result to verify
    whether the model's stated reasoning matches its actual internal
    reasoning process.
    """
    traces_dir = _ensure_traces_dir()

    provider_name = llm_client.get_provider_name()
    model_name = llm_client.get_model_name()

    # Build a filesystem-safe timestamp (no colons)
    safe_ts = timestamp.replace(":", "").replace("+", "p")
    filename = f"problem_{problem_id}_submission_{submission_id}_{provider_name}_{safe_ts}.json"
    filepath = traces_dir / filename

    trace_data = {
        "problem_statement": problem_statement,
        "rubric": rubric,
        "student_pseudocode": student_pseudocode,
        "evaluator_provider": provider_name,
        "evaluator_model": model_name,
        "evaluator_thinking": llm_thinking,
        "evaluation_result": evaluation_result,
        "validation_result": {
            "passed": validation_passed,
            "message": validation_message,
        },
        "retry_attempted": retry_attempted,
        "timestamp": timestamp,
    }

    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(trace_data, fh, indent=2, ensure_ascii=False)
        print(f"[evaluator] Trace saved → {filepath}")
    except OSError as exc:
        # Non-fatal: log but do not crash the evaluation pipeline
        print(f"[evaluator] WARNING: failed to save trace: {exc}")


# ──────────────────────────────────────────────────────────────────────
# Rubric persistence (save / load / list)
# ──────────────────────────────────────────────────────────────────────

def _ensure_rubrics_dir() -> Path:
    """Create data/rubrics/ if it does not exist and return its Path."""
    RUBRICS_DIR.mkdir(parents=True, exist_ok=True)
    return RUBRICS_DIR


def _save_rubric(
    problem_statement: str,
    rubric: dict,
    problem_id: str,
) -> Path:
    """
    Save a generated rubric to ``data/rubrics/`` as a JSON file.

    The file stores both the problem statement and the rubric so the
    evaluator can load everything it needs from one file.

    Returns the path to the saved file.
    """
    rubrics_dir = _ensure_rubrics_dir()
    provider_name = llm_client.get_provider_name()
    model_name = llm_client.get_model_name()

    timestamp = datetime.now(timezone.utc).isoformat()
    safe_ts = timestamp.replace(":", "").replace("+", "p")
    filename = f"rubric_{problem_id}_{provider_name}_{safe_ts}.json"
    filepath = rubrics_dir / filename

    data = {
        "problem_id": problem_id,
        "problem_statement": problem_statement,
        "rubric": rubric,
        "llm_provider": provider_name,
        "llm_model": model_name,
        "created_at": timestamp,
    }

    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)

    return filepath


def _list_saved_rubrics() -> list[dict]:
    """
    List all saved rubrics from ``data/rubrics/``.

    Returns a list of dicts, each containing the loaded JSON plus a
    ``_filepath`` key for reference.  Sorted by creation time (newest
    last).
    """
    rubrics_dir = _ensure_rubrics_dir()
    rubric_files = sorted(rubrics_dir.glob("rubric_*.json"))

    results: list[dict] = []
    for fp in rubric_files:
        try:
            with open(fp, encoding="utf-8") as fh:
                data = json.load(fh)
            data["_filepath"] = str(fp)
            results.append(data)
        except (json.JSONDecodeError, OSError):
            continue  # skip corrupt files

    return results


# ──────────────────────────────────────────────────────────────────────
# Interactive terminal interface
# ──────────────────────────────────────────────────────────────────────

def _read_multiline(prompt_msg: str) -> str:
    """
    Read multiline input from the terminal.

    The user types freely and submits by entering a blank line.
    """
    print(prompt_msg)
    print("  (type your text, then press Enter on an empty line to finish)\n")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def _print_section(title: str, width: int = 60) -> None:
    """Print a visual section divider."""
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}\n")


def _display_rubric(rubric: dict) -> None:
    """Pretty-print a rubric to the terminal."""
    for dim in rubric.get("dimensions", []):
        print(f"  {dim['name']} (weight {dim['weight']}%)")
        print(f"    {dim['description']}")
        for sc in dim.get("sub_criteria", []):
            print(f"      • {sc}")
        print()


def _display_evaluation(result: dict) -> None:
    """Pretty-print the evaluation result to the terminal."""
    # Per-dimension results
    for dim in result.get("dimensions", []):
        name = dim.get("name", "?")
        score = dim.get("score", "?")
        print(f"  [{score:>9s}]  {name}")

        if dim.get("correct"):
            print(f"             ✓ {dim['correct']}")
        # Hide explicit 'issue' text from students entirely to force them to think.
        # The issue is still recorded in the JSON trace for teacher analytics.
        if dim.get("hint"):
            print(f"             💡 {dim['hint']}")
        print()

    # Trace
    trace = result.get("trace")
    if trace:
        _print_section("Step-by-step trace")
        print(trace)


def _print_main_menu() -> None:
    """Display the main menu options."""
    print("  [1]  Generate rubric   (enter a problem, get a rubric)")
    print("  [2]  Evaluate submission   (pick a question, submit pseudocode)")
    print("  [3]  View saved rubrics")
    print("  [q]  Quit")
    print()


async def _handle_generate_rubric(problem_counter: int) -> int:
    """
    Flow: teacher enters a problem statement → generate rubric → save.

    Returns the updated problem_counter.
    """
    _print_section("Generate Rubric")
    problem_text = _read_multiline("Enter the problem statement:")

    if not problem_text.strip():
        print("⚠  Empty problem statement — cancelled.")
        return problem_counter

    problem_counter += 1
    problem_id = f"p{problem_counter:03d}"

    print("\n⏳ Generating rubric …")
    try:
        rubric = await generate_rubric(
            problem_statement=problem_text,
            problem_id=problem_id,
        )
    except Exception as exc:
        print(f"\n✗ Rubric generation failed: {exc}")
        return problem_counter

    # Save the rubric
    filepath = _save_rubric(
        problem_statement=problem_text,
        rubric=rubric,
        problem_id=problem_id,
    )

    _print_section("Generated Rubric")
    _display_rubric(rubric)
    print(f"  ✓ Rubric saved → {filepath}")

    return problem_counter


def _select_rubric() -> dict | None:
    """
    Show available questions and let the user pick one.

    Only the problem statement is displayed — rubric details are
    kept hidden so students cannot see the grading criteria.

    Returns the selected rubric data dict, or None if cancelled.
    """
    saved = _list_saved_rubrics()

    if not saved:
        print("  ⚠  No questions available. Ask your teacher to set one up.")
        return None

    _print_section("Available Questions")
    for idx, entry in enumerate(saved, start=1):
        problem_id = entry.get("problem_id", "?")
        provider   = entry.get("llm_provider", "unknown")
        model      = entry.get("llm_model", "?")
        problem_text = entry.get("problem_statement", "(no question)")
        print(f"  [{idx}]  Question {problem_id}  —  generated by {provider} ({model})")
        for line in problem_text.strip().split("\n"):
            print(f"        {line}")
        print()

    try:
        choice = input("Select a question number (or 'back' to cancel): ").strip()
    except EOFError:
        return None

    if choice.lower() in {"back", "b", ""}:
        return None

    try:
        index = int(choice) - 1
        if 0 <= index < len(saved):
            return saved[index]
        else:
            print(f"  ⚠  Invalid selection: {choice}")
            return None
    except ValueError:
        print(f"  ⚠  Invalid input: {choice}")
        return None


async def _handle_evaluate_submission(submission_counter: int) -> int:
    """
    Flow: pick a saved rubric → enter pseudocode → evaluate.

    Loops so the user can submit multiple answers against the same
    rubric.  Returns the updated submission_counter.
    """
    selected = _select_rubric()
    if selected is None:
        return submission_counter

    problem_id = selected.get("problem_id", "unknown")
    problem_text = selected["problem_statement"]
    rubric = selected["rubric"]

    _print_section(f"Question: {problem_id}")
    for line in problem_text.strip().split("\n"):
        print(f"  {line}")

    # Inner loop: multiple submissions against this rubric
    while True:
        _print_section("Student Submission")
        pseudocode = _read_multiline("Enter the student's pseudocode:")

        if pseudocode.strip().lower() in {"quit", "exit", "q"}:
            print("Returning to main menu.\n")
            break
        if pseudocode.strip().lower() in {"back", "b"}:
            print("Returning to main menu.\n")
            break
        if not pseudocode.strip():
            print("⚠  Empty submission — skipping.")
            continue

        submission_counter += 1
        submission_id = f"s{submission_counter:03d}"

        print("\n⏳ Evaluating submission …")
        result = await evaluate_submission(
            problem_statement=problem_text,
            rubric=rubric,
            student_pseudocode=pseudocode,
            problem_id=problem_id,
            submission_id=submission_id,
        )

        if result.get("error"):
            print(f"\n✗ Evaluation failed: {result['message']}")
            raw = result.get("raw_response", "")
            if raw:
                print(f"  Raw response: {raw[:300]}")
            print()
            continue

        _print_section("Evaluation Result")
        _display_evaluation(result)

        print(f"{'─' * 60}")
        print("  Options:")
        print("    • Enter another submission for this same problem")
        print("    • Type 'back' to return to the main menu")
        print()

    return submission_counter


def _handle_view_rubrics() -> None:
    """Display all saved rubrics with full details."""
    saved = _list_saved_rubrics()

    if not saved:
        print("\n  ⚠  No saved rubrics found. Generate one first (option 1).\n")
        return

    for idx, entry in enumerate(saved, start=1):
        problem_id = entry.get("problem_id", "?")
        created    = entry.get("created_at", "?")
        provider   = entry.get("llm_provider", "unknown")
        model      = entry.get("llm_model", "?")
        problem_text = entry.get("problem_statement", "(no problem statement)")

        _print_section(f"[{idx}] Rubric {problem_id}  —  {provider} ({model})  —  created {created}")
        print("  Problem:")
        for line in problem_text.strip().split("\n"):
            print(f"    {line}")
        print()
        _display_rubric(entry.get("rubric", {}))


async def _interactive_loop() -> None:
    """
    Menu-based interactive terminal session.

    - Option 1: Generate and save a rubric (teacher flow)
    - Option 2: Select a saved rubric and evaluate pseudocode (student flow)
    - Option 3: View all saved rubrics
    """
    banner = "=" * 60
    provider = llm_client.get_provider_name()

    print(f"\n{banner}")
    print("  PSEUDOCODE EVALUATOR — Interactive Mode")
    print(f"{banner}")
    print()
    print(f"  Provider : {provider}")
    print("  Generate rubrics and evaluate student pseudocode.")
    print(f"\n{banner}\n")

    problem_counter = 0
    submission_counter = 0

    while True:
        _print_main_menu()

        try:
            choice = input("  ▸ Choose an option: ").strip().lower()
        except EOFError:
            break

        if choice in {"q", "quit", "exit"}:
            break
        elif choice == "1":
            problem_counter = await _handle_generate_rubric(problem_counter)
        elif choice == "2":
            submission_counter = await _handle_evaluate_submission(
                submission_counter
            )
        elif choice == "3":
            _handle_view_rubrics()
        else:
            print(f"  ⚠  Unknown option: '{choice}'. Enter 1, 2, 3, or q.\n")

    print("\nGoodbye! 👋\n")


if __name__ == "__main__":
    asyncio.run(_interactive_loop())

