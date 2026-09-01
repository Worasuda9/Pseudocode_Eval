# FILE: 07_prompts_audit.txt
# DESCRIPTION: Full audit of initial prompt structure and identified issues
# SOURCE: prompts_audit.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Prompts v3 Audit

## Issue 1: Double-negative / negative phrasing → positive commands

These lines use "Do NOT" or "Never" where a positive instruction says the same thing more clearly.

### RUBRIC_SYSTEM_PROMPT (Call 1)

| Line | Current (negative) | Proposed (positive) |
|------|-------------------|-------------------|
| 80 | `not too code-like, not too vague` | `at a balanced abstraction level — concrete enough to follow but not literal code` |
| 87–90 | `Do NOT penalise for missing indentation, formatting style, or layout. Clarity means logical readability only. Do NOT penalise informal, plain, or casual word choice as long as the reference is still clear.` | `Evaluate logical readability only — ignore indentation, formatting, and layout. Accept informal or casual word choice as long as the meaning is clear.` |
| 109 | `Do not write a model answer or correct solution` | `Omit model answers and correct solutions` |
| 110 | `Do not add extra dimensions beyond the 4 listed` | `Use only the 4 dimensions listed above` |

### EVALUATION_SYSTEM_PROMPT (Call 2)

| Line | Current (negative) | Proposed (positive) |
|------|-------------------|-------------------|
| 159–161 | `Do not solve anything yet — just identify what is involved.` | *(this one is fine — it's a sequencing instruction, not a scoring rule)* |
| 200 | `Do NOT give credit for structure alone if the logic is wrong` | `Credit logic correctness only — structure without correct logic is insufficient` |
| 221–225 | `Do NOT penalise for missing indentation, formatting, or layout. Clarity is about logical understandability, not visual style. Do NOT penalise informal, plain, or casual word choice (e.g. "stuff", "thing") as long as what it refers to is still clear from context` | `Evaluate logical understandability only — ignore indentation, formatting, and layout. Accept informal or casual word choice (e.g. "stuff", "thing") as long as the referent is clear from context.` |
| 240–241 | `Only evaluate what is explicitly written — do not assume or infer steps the student did not write` | `Evaluate only what is explicitly written — treat missing steps as absent, with no assumptions` |
| 242 | `Never reveal the correct solution or write corrected pseudocode` | `Keep the correct solution hidden — provide only hints and feedback` |
| 243 | `Never fabricate a positive "correct" note on a Fair or Poor dimension` | `Leave "correct" as null when nothing was genuinely done well for that dimension` |
| 246 | `Hints must be under 20 words and must not state the answer directly` | `Hints must be under 20 words and guide discovery rather than stating the answer` |

---

## Issue 2: Inconsistent dimension definitions between Call 1 and Call 2

The rubric prompt (Call 1) and evaluation prompt (Call 2) should use **identical** dimension definitions so the evaluator grades against exactly what the rubric was designed around. Here are the mismatches:

### CORRECTNESS
| Aspect | Call 1 (rubric) | Call 2 (evaluation) |
|--------|----------------|---------------------|
| Bullet 2 wording | `functional correctness — simulated through mental tracing, not execution` | `functional correctness — simulated through mental tracing, not execution` |  
| Extra bullet | *(none)* | `Do NOT give credit for structure alone if the logic is wrong` |

> **Verdict**: Minor mismatch — Call 2 adds a grading instruction. **Acceptable** since that bullet is evaluator guidance, not a definition.

### COMPLETENESS
| Aspect | Call 1 (rubric) | Call 2 (evaluation) |
|--------|----------------|---------------------|
| Bullet 4 (termination) | ✅ `Whether stopping or termination conditions are concrete and checkable (e.g. "loop until the counter reaches the list length") rather than vague or indeterminate (e.g. "keep going until done")` | ✅ `Check whether stopping/termination conditions are concrete and checkable (e.g. "until the index reaches the end of the list") rather than vague or indeterminate (e.g. "keep going until done", "repeat until finished")` |

> **Verdict**: **Inconsistent examples** — Call 1 uses `"loop until the counter reaches the list length"`, Call 2 uses `"until the index reaches the end of the list"`. Also Call 2 adds `"repeat until finished"` as a bad example. Should unify.

### CLARITY
| Aspect | Call 1 (rubric) | Call 2 (evaluation) |
|--------|----------------|---------------------|
| Bullet 3 | `Whether variable or quantity references are unambiguous — each reference to "it", "that value", or "the number" should clearly map to one specific thing, not be reusable for multiple different values` | `Check whether each reference to a value, variable, or quantity is unambiguous — flag cases where "it", "that", or "the number" could refer to more than one thing in context` |
| Bullet 4 | `Whether variable names and step descriptions are meaningful and unambiguous` | `Check whether variable names and descriptions are meaningful` |

> **Verdict**: **Inconsistent** — different wording, Call 2 drops "step descriptions" and "unambiguous" from bullet 4. Should unify.

### EFFICIENCY
| Aspect | Call 1 (rubric) | Call 2 (evaluation) |
|--------|----------------|---------------------|
| All bullets | Match ✅ | Match ✅ |
| Extra Call 2 bullet | *(none)* | `Be lenient for CS1 students: only mark Poor if there is a clear algorithmic inefficiency` |

> **Verdict**: Acceptable — the leniency note is evaluator-specific guidance.

---

## Issue 3: Other problems found

### 3a. Call 1 clarity bullet combines two separate concerns
Line 82–86 has a long bullet about "unambiguous references" followed by a separate bullet about "meaningful variable names" — but the unambiguous-references bullet already covers variable naming. These could be combined or the second one trimmed to avoid redundancy.

### 3b. "not too code-like, not too vague" appears only in Call 1
Line 80 in the Clarity definition uses `not too code-like, not too vague`. Call 2 just says `at the right abstraction level`. Should be consistent — recommend using the positive phrasing in both.

### 3c. Call 2 has 5 evaluation steps, Call 1 has 3
This is by design (Call 2 is more complex), so it's fine. Just noting for completeness.

### 3d. `student_level` removed from EVALUATION_USER_PROMPT_TEMPLATE but still referenced
Line 247–249 of Call 2's system prompt says *"Match hint language complexity to student level: simpler, encouraging language for beginner; more technical for intermediate"*, but the user prompt template (lines 320–328) has **no `{student_level}` placeholder**. The model receives no student level info. This is either a bug, or student_level was intentionally removed. **Needs clarification.**

---

## Summary of recommended changes

| # | Category | Action |
|---|----------|--------|
| 1 | Double negatives | Rewrite ~10 phrases from "Do NOT X" to positive commands |
| 2 | Consistency | Unify dimension definitions: use **one canonical version** of each dimension's bullets in both prompts, then add Call-2-only evaluator guidance separately |
| 3a | Redundancy | Merge or trim the two clarity bullets about variable naming |
| 3b | Phrasing | Use consistent "balanced abstraction level" wording in both prompts |
| 3d | Bug? | Either restore `{student_level}` to the user prompt template, or remove the student-level hint guidance from the system prompt |
