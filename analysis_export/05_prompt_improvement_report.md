# FILE: 05_prompt_improvement_report.txt
# DESCRIPTION: Detailed report on 7 targeted prompt fixes and their impact
# SOURCE: prompt_improvement_report.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Prompt Improvement Report
## Changes made to `prompts.py` based on combined disagreement analysis (132 cases)

---

## Overview of Changes

| Fix | Category | Location in prompts.py | Cases addressed |
|---|---|---|---|
| 1 | C — Rubric prescription | `RUBRIC_SYSTEM_PROMPT` Rules section | 16 cases (12%) |
| 2 | D — Dimension confusion | `EVALUATION_SYSTEM_PROMPT` Additional notes | 8 cases (6%) |
| 3 | B — Absence penalization | `EVALUATION_SYSTEM_PROMPT` Additional notes | Reinforced existing rule |
| 4 | G — LLM hallucination (Clarity) | `EVALUATION_SYSTEM_PROMPT` Additional notes | 6 cases (5%) |
| 5 | C — Completeness implied output | `EVALUATION_SYSTEM_PROMPT` Additional notes | Subset of 16 C-cases |

Categories **A (LLM systematic strictness, 53%)**, **F (LLM leniency, 13%)**, and **HE (Human error, 11%)** are not fixed by prompts:
- **A** reflects a calibration gap between human and LLM — some of this is the LLM being appropriately strict; the rubric fixes (Fix 1) will reduce the unwarranted portion
- **F** is the LLM being too lenient on some cases — documented, not fixed, as these are often edge cases where the human was actually stricter than necessary
- **HE** requires human rater re-calibration, not a prompt change

---

## Fix 1 — Rubric Prescription (C)

**Category:** C — Rubric prescription  
**Evidence from data:** 16 cases, all 4 pairs  
**Consistent patterns found:**
- P3/correct/COM (all 4 pairs): LLM deducted because student didn't write an explicit `print` statement. The rubric sub-criterion "Outputs the final vowel and consonant counts" was applied as requiring a literal print command.
- P4/correct/COM (all 4 pairs): LLM deducted because student wrote "the function takes two numbers" instead of `FUNCTION calculation(a, b)`. The rubric sub-criterion required the keyword "FUNCTION".
- P2/correct/EFF (all 4 pairs): LLM deducted because membership check on output list implies O(n²). The rubric sub-criterion "avoids repeatedly scanning the result list" penalized the most natural correct approach for CS1.

**What was wrong:** The rubric generator was writing sub-criteria that required:
1. Formal keyword syntax (FUNCTION, FOR, RETURN)
2. Explicit output statements even when the algorithm implied them
3. Efficiency standards that penalized common introductory approaches

**What was changed in** `RUBRIC_SYSTEM_PROMPT`:
```
[FIX: Rubric prescription]
- NEVER require formal programming syntax in sub-criteria. A student
  who writes "the function takes two numbers" fully satisfies a
  "function definition" sub-criterion.
- NEVER require an explicit print/output statement as its own
  Completeness sub-criterion. Only flag missing output if no output
  mechanism whatsoever is described.
- Efficiency sub-criteria must target genuine computational choices.
  NEVER write a sub-criterion that penalizes a correct algorithm for
  using a common introductory approach (e.g. list membership check
  for CS1 is acceptable).
- Do not write sub-criteria that penalize absence of a step that is
  clearly implied by the surrounding context.
```

**Expected effect:** Newly generated rubrics will not penalize students for informal language or missing syntactic keywords. Completeness will only require structural presence, not formal notation.

---

## Fix 2 — Dimension Confusion in Efficiency (D)

**Category:** D — Dimension confusion  
**Evidence from data:** 8 cases, all 4 pairs (exact same 2 cases per pair)  
**Consistent patterns found:**
- **P2/partially_correct/EFF** (all 4 pairs): LLM gave Poor for Efficiency because the algorithm "only handles adjacent duplicates." But adjacent comparison is O(N) — efficient. The real flaw is Correctness scope (wrong problem). Efficiency charged incorrectly.
- **P5/largely_incorrect/EFF** (all 4 pairs): LLM gave Poor for Efficiency because "infinite recursion is inefficient." But infinite recursion (calling with the same argument, no base case) is a **Correctness** failure — the algorithm never terminates. This is not an efficiency problem.

**What was wrong:** The evaluator conflated "algorithm is wrong" with "algorithm is inefficient." When an algorithm fails at Correctness, the LLM sometimes also penalized Efficiency, double-penalizing and mis-categorizing the root cause.

**What was changed in** `EVALUATION_SYSTEM_PROMPT`:
```
[FIX: Dimension confusion — Efficiency]
- CRITICAL: Efficiency evaluates computational performance only —
  whether the approach avoids redundant work. It does NOT evaluate
  whether the algorithm is logically correct.
- Ask yourself: "Is this algorithm wrong, or is it correct but slow?"
  Only the latter warrants an Efficiency deduction.
- Infinite recursion is a Correctness failure — never penalize under Efficiency.
- An algorithm handling only adjacent duplicates is a Correctness scope
  issue — not an Efficiency issue. A single O(N) pass is efficient.
- Do not score Efficiency as Poor merely because an algorithm is incorrect.
```

**Also removed** the rule: `"If the submission lacks concrete algorithmic steps, score Efficiency as Poor with issue: 'Insufficient algorithmic detail to assess efficiency.'"` — this was the root cause of several LLM hallucination cases where the LLM used this boilerplate on submissions that did have describable logic.

**Expected effect:** Efficiency Poor will only fire for genuinely redundant operations (nested loops, repeated full scans). Correctness failures will stay in Correctness.

---

## Fix 3 — Absence Penalization (B)

**Category:** B — Absence penalization  
**Evidence from data:** 1 direct case; also underlies many Category A cases  
**Pattern:** LLM penalized for missing an explicit output line even when the student described a complete algorithm. Also penalized informal loop descriptions ("go through each element") as if no loop was present.

**What was changed in** `EVALUATION_SYSTEM_PROMPT`:
```
[FIX: Absence penalization]
- Treat clearly implied steps as present. If a student describes a
  complete algorithm and the final output is implied by the problem
  statement, do not penalize Completeness for missing an explicit line.
- A student who writes "the function takes two numbers" has satisfied
  a function-definition requirement.
- Structural intent counts. If a student says "go through each element"
  without writing "FOR i FROM 0 TO N-1", the loop is present.
```

**Expected effect:** Evaluation will credit clearly implied structure rather than penalizing for missing keyword formality.

---

## Fix 4 — LLM Hallucination in Clarity (G)

**Category:** G — LLM hallucination  
**Evidence from data:** 6 cases total; 3 per Gemini pair, 0 in OpenAI pairs  
**Consistent pattern found:**
- **P1/incorrect/CLA** (both Gemini pairs): Student wrote "I check if the number is bigger than 5. If it is, I print 120." — clearly wrong logic but clearly *written*. Gemini gave **Excellent** for Clarity. Rater1 gave Poor, Rater2 gave Fair. Gap of 2–3 levels.
- **P4/partially_correct/EFF and P4/largely_incorrect/EFF** (both Gemini pairs): Gemini gave **Excellent** for Efficiency to an incomplete/incorrect function. No efficiency justification exists.

**Root cause of Clarity hallucination:** The LLM was awarding Excellent Clarity when the pseudocode was clearly written — even for submissions with very wrong logic. The human raters, seeing clearly wrong answers, intuitively downgraded Clarity (conflating it with Correctness). Both sides were partially wrong: the LLM should have given Good/Fair (not Excellent) for Clarity when the description is readable but the intent is unclear or nonsensical. The human should not conflate Clarity with Correctness.

The deeper hallucination problem (Efficiency Excellent on wrong functions) was caused by the boilerplate rule "If operations are sequential with no redundancy, score Excellent" — applied without checking if the operations even do what the problem requires.

**What was changed in** `EVALUATION_SYSTEM_PROMPT`:
```
[FIX: Clarity hallucination prevention]
- Clarity evaluates ONLY readability — completely independent of
  whether the algorithm is correct.
- A clearly written wrong answer scores Excellent or Good on Clarity
  if the steps are easy to follow.
- NEVER let Correctness or Completeness scores influence your Clarity score.
- Ask: "Can I follow what the student is trying to do, step by step?"
  If yes, Clarity is at least Fair.
```

**Expected effect:** Clarity scores will be consistent regardless of algorithm correctness. No more 3-level gaps like Poor vs Excellent on the same submission.

---

## Fix 5 — Completeness: Implied Output (C subset)

**Category:** C — Rubric prescription (Completeness dimension specifically)  
**Evidence:** Recurring across all 4 pairs in P3/correct/COM and P4/correct/COM  
**Pattern:** Gemini and OpenAI both deducted from Excellent→Good because the student did not write a literal `print vowels, consonants` or `return both values` line at the end of an otherwise complete algorithm.

**What was changed in** `EVALUATION_SYSTEM_PROMPT`:
```
[FIX: Completeness — implied output]
- If the algorithm describes all computation steps and the problem
  obviously requires output, the output sub-criterion is satisfied
  even without a literal "print" or "return" statement.
- Only deduct for missing output if the student described NO output
  mechanism at all and the output is non-trivial to infer.
```

**Expected effect:** Well-described algorithms that clearly compute the right answer will score Excellent on Completeness even without an explicit output command at the end.

---

## What Was NOT Changed (and Why)

| Category | Count | Decision |
|---|---|---|
| A — LLM systematic strictness | 70 (53%) | Not a prompt bug — reflects genuine LLM calibration. Fix 1 will reduce the rubric-driven portion. The remaining gap is a calibration difference that requires human rater calibration or score-level adjustment |
| F — LLM leniency | 17 (13%) | Documented but not fixed. These are cases where the LLM was more generous than the human. Some are correct (e.g. the LLM correctly gave Excellent to a clearly written wrong answer on Clarity) |
| HE — Human error | 14 (11%) | Requires human rater re-calibration, not a prompt change. The 3 most consistent cases (P2/largely_incorrect/COR, P2/incorrect/COR, P4/incorrect/COM) should be flagged for rater review |

---

## Summary of Files Changed

| File | What changed |
|---|---|
| [`prompts.py`](file:///Users/fofafaii/Desktop/pseudocode_evaluation_system/prompts.py) | `RUBRIC_SYSTEM_PROMPT`: Added Fix 1 block (rubric prescription rules) |
| [`prompts.py`](file:///Users/fofafaii/Desktop/pseudocode_evaluation_system/prompts.py) | `EVALUATION_SYSTEM_PROMPT`: Added Fix 2 block (Efficiency dimension confusion) |
| [`prompts.py`](file:///Users/fofafaii/Desktop/pseudocode_evaluation_system/prompts.py) | `EVALUATION_SYSTEM_PROMPT`: Added Fix 3 block (Absence penalization) |
| [`prompts.py`](file:///Users/fofafaii/Desktop/pseudocode_evaluation_system/prompts.py) | `EVALUATION_SYSTEM_PROMPT`: Added Fix 4 block (Clarity hallucination) |
| [`prompts.py`](file:///Users/fofafaii/Desktop/pseudocode_evaluation_system/prompts.py) | `EVALUATION_SYSTEM_PROMPT`: Added Fix 5 block (Completeness implied output) |
| [`prompts.py`](file:///Users/fofafaii/Desktop/pseudocode_evaluation_system/prompts.py) | `EVALUATION_SYSTEM_PROMPT`: **Removed** the boilerplate "Insufficient algorithmic detail" Efficiency rule that caused hallucinations |
