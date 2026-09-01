# FILE: 11_evaluation_audit.txt
# DESCRIPTION: Evaluation pipeline audit — trace inspection and validation
# SOURCE: evaluation_audit.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Evaluation Results Audit — Full Trace Analysis

## Overview

Reviewed **39 trace files** across **8 problems** covering: factorial, list sum, bubble sort, linear search, find max / recursive sum, inner/outer functions, income tax, and leap year.

- **Validation pass rate:** 36/39 first attempt (92%), all 39 passed after retry
- **Retry rate:** 3/39 required retry (8%)
- **All 3 retries** failed with the same error: `Issue must not be null when score is Good for Clarity`

---

## 1. Scoring Accuracy — ✅ Generally Good

The model correctly differentiates quality levels:

| Student Answer Quality | Example | Scores Given | Verdict |
|---|---|---|---|
| Perfect algorithm | p004/s012 (linear search with position tracking) | All Excellent | ✅ Correct |
| Correct but informal | p002/s003 ("go through each item, add to total") | Excellent/Excellent/Good/Excellent | ✅ Correct |
| Partially correct | p008/s011 (leap year — checks 400/100/4 but no input/output) | Good/Fair/Fair/Excellent | ✅ Correct |
| Vague but right direction | p005/s001 ("remember biggest one") | Fair/Fair/Good/Good | ✅ Correct |
| Fundamentally wrong | p008/s009 (20% flat tax on all income) | Poor/Poor/Fair/Poor | ✅ Correct |
| Non-attempt | p003/s009 ("sort the numbers, done") | All Poor | ✅ Correct |
| Completely wrong logic | p006/s005 (inner function adds 5 to a, outer adds 5 to b) | All Poor | ✅ Correct |

---

## 2. Thinking Tokens — ✅ Genuine Reasoning

| Aspect | Finding |
|---|---|
| **Substantive?** | Yes — real step-by-step analysis, self-corrections, bracket calculations, etc. |
| **Matches trace?** | Yes — trace is a formalized condensation of thinking |
| **Contradictions?** | None observed |
| **Hallucination signs?** | None — thinking references actual student pseudocode text |

**Example (p007/s007 — income tax, hardcoded $45k):**
- **Thinking:** *"The student performed manual calculation for $45,000 specifically... this is a narrative, not a general algorithm..."*
- **Trace:** Labels structural categories correctly, identifies the hardcoded nature
- **Score:** Correctness: Fair — consistent ✅

---

## 3. Issues Found

### Issue A — 🔴 HIGH: "Good + null issue" still triggers validation failure

**Evidence:** 3 traces failed validation with:
```
Issue must not be null when score is Good for Clarity
```

All 3 are for the same leap year pseudocode (even/odd check) where the model scored Clarity as **Good** with **issue: null**.

**What happened:** We fixed the prompts.py rules in the previous session, but these traces are from the 06-24 run — **before** the fix was deployed. After retry, the model corrected itself and provided an issue string.

> [!IMPORTANT]
> **Status:** This was already fixed in the previous session. The 3 retries confirm the validator caught the problem correctly and the retry mechanism worked. **No further action needed** — but you should verify on your next test run that the retry rate drops to 0%.

---

### Issue B — 🟡 MEDIUM: Correctness penalized for efficiency concerns

| Submission | Pseudocode | Correctness | Issue cited |
|---|---|---|---|
| p008/s001 (prime) | "while divisor < number" (checks up to n−1) | **Good** | "Loop runs up to number-1 instead of sqrt(number)" |
| p006/s004 (reverse string) | "start from last letter, go backwards" | **Good** | "Does not explicitly state the loop's concrete stopping condition" |

For the prime checker: The algorithm **produces correct results for all inputs**. Checking up to n−1 vs sqrt(n) is an **efficiency** choice, not a correctness error. This should be:
- Correctness: **Excellent** (logic is correct)
- Efficiency: **Good** (suboptimal range)

> [!WARNING]
> **Fix needed in prompts.py evaluator notes:**
> Add: *"Score Correctness based solely on whether the logic produces correct output for all valid inputs. Suboptimal algorithmic choices (e.g. checking divisors up to n instead of √n) are Efficiency concerns, not Correctness concerns."*

---

### Issue C — 🟡 MEDIUM: Same gap penalized in two dimensions

| Submission | Gap | Dimensions penalized |
|---|---|---|
| p007/s010 (vowel count) | "No explicit initialization of count" | Correctness: Good **and** Completeness: Good |
| p005/s001 (find max) | "No explicit initialization" | Correctness: Fair **and** Completeness: Fair |
| p008/s012 (leap year) | "Only checks div by 4, not 100/400" | Correctness: Poor **and** Completeness: Fair |

Students are double-penalized for a single gap. Missing initialization is a **Completeness** issue; it should only affect Correctness if the algorithm would produce **wrong results** because of it.

> [!NOTE]
> **Fix needed in prompts.py evaluator notes:**
> Add: *"Each specific gap should be attributed to the single most relevant dimension. Missing initialization is a Completeness issue — only flag it under Correctness if the omission causes incorrect results."*

---

### Issue D — 🟡 MEDIUM: Clarity scoring is inconsistent for code-like syntax

| Submission | Syntax used | Clarity Score | Issue cited |
|---|---|---|---|
| p003/s010 (bubble sort) | `list[j] > list[j+1]` | Good | "uses code-like syntax" |
| p004/s014 (linear search) | `list[i] equals target` | Good | "uses code-like syntax" |
| p008/s012 (prime) | `n mod i = 0` | Excellent | (no issue) |

Array indexing penalized, but `mod` operator is not. Both are standard pseudocode conventions.

> [!NOTE]
> **Fix needed in `_DIMENSION_DEFINITIONS` (Clarity):**
> Add: *"Standard pseudocode notation such as array indexing (list[i]), mathematical operators (mod, ×), and comparison symbols are acceptable — evaluate readability of the logic, not whether notation resembles code."*

---

### Issue E — 🟢 LOW: Efficiency scoring inconsistent for vague submissions

| Submission | Content | Efficiency |
|---|---|---|
| p006/s003 (reverse string) | "take a word, make it backwards, show it" | **Poor** |
| p002/s005 (list sum) | "take each number, add them all up, tell the answer" | **Fair** |
| p004/s013 (linear search) | "look through the list, find the thing, tell where it is" | **Poor** |

All three are equally vague with no concrete algorithmic steps, but one gets Fair. 

> [!NOTE]
> **Recommendation:** Add rule: *"If the submission lacks concrete algorithmic steps, Efficiency should be scored Poor with issue: 'Insufficient algorithmic detail to assess efficiency.'"*

---

## 4. Hint Quality — ✅ Consistently Good

All Socratic hints are:
- ✅ Under 20 words
- ✅ Guiding without revealing
- ✅ Problem-specific, not generic
- ✅ Only present for Fair/Poor scores (after our fix)

**Good examples:**
- *"What value does 'biggest one' start as before you see any number?"*
- *"How does a recursive function ensure it eventually stops?"*
- *"What are the specific mathematical rules for a leap year, beyond just being even?"*

---

## 5. Consistency Across Identical Submissions — ✅ Deterministic

Three traces contain **identical pseudocode** (even/odd leap year check): p008/s001, p008/s014, p008/s015. All three received **identical scores** and **nearly identical feedback**. Temperature=0 is working as intended.

---

## Summary of Required Fixes

| # | Priority | Issue | Location |
|---|---|---|---|
| **A** | ✅ Already fixed | Good + null issue validation | prompts.py (done last session) |
| **B** | 🔴 High | Correctness penalized for efficiency concerns | prompts.py — evaluator notes |
| **C** | 🟡 Medium | Same gap penalized in two dimensions | prompts.py — evaluator notes |
| **D** | 🟡 Medium | Code-like syntax inconsistency | prompts.py — `_DIMENSION_DEFINITIONS` |
| **E** | 🟢 Low | Vague submission efficiency inconsistency | prompts.py — evaluator notes |

Want me to apply fixes B–E to `prompts.py`?
