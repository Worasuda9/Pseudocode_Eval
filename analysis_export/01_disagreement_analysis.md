# FILE: 01_disagreement_analysis.txt
# DESCRIPTION: Root cause analysis of LLM vs human disagreements (initial 5 problems)
# SOURCE: disagreement_analysis.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Disagreement Cause Analysis
## Human Raters vs. LLM Evaluators — All 4 Comparison Pairs
**Problems: P1–P5 | 5 problems × 4 levels × 4 dimensions = 80 score cells per pair**

---

## Category Definitions

| # | Category | Description |
|---|---|---|
| **1** | **Rubric prescription** | The rubric's sub-criteria are too strict or literal, causing a penalty that doesn't reflect real learning value (e.g., docking for missing the word "FUNCTION" in pseudocode) |
| **2** | **Dimension confusion** | The gap is real but attributed to the wrong dimension (e.g., an Efficiency score penalized for a Correctness flaw like infinite recursion) |
| **3** | **Legitimate disagreement** | Both scores are defensible. Reasonable evaluators could disagree based on how strictly they apply the rubric |
| **4** | **Human error** | The human score is clearly wrong — over-crediting fundamentally incorrect logic, or under-crediting clearly correct logic |
| **5** | **LLM hallucination** | The LLM cited an issue that doesn't actually exist in the student's pseudocode, or fabricated a flaw |

---

## Aggregated Results Across All 4 Pairs

| Category | rater1 vs Gemini | rater1 vs OpenAI | rater2 vs Gemini | rater2 vs OpenAI | **Total** | **%** |
|---|---|---|---|---|---|---|
| **Rubric prescription** | 4 | 4 | 4 | 6 | **18** | **17%** |
| **Dimension confusion** | 5 | 2 | 4 | 2 | **13** | **12%** |
| **Legitimate disagreement** | 17 | 13 | 14 | 14 | **58** | **55%** |
| **Human error** | 5 | 6 | 6 | 6 | **23** | **22%** |
| **LLM hallucination** | 0 | 2 | 0 | 0 | **2** | **2%** |
| **Total disagreements** | **31** | **27** | **28** | **28** | **114** | **100%** |

> Note: Totals are counted per pair independently; the same disagreement may appear across multiple pairs if both raters disagreed with the LLM on the same case.

---

## Highlighted Findings Per Category

---

### 🔵 1. Rubric Prescription (18 cases, 17%)

These are cases where the rubric's literal sub-criteria caused the LLM to penalize something that a human educator would accept as adequate.

**Most common trigger:** The Completeness dimension across all problems contains sub-criteria for explicit edge-case handling (N=0, empty inputs) and formal syntax ("FUNCTION calculation(param1, param2)"). These appear in every problem's rubric and consistently caused Completeness scores to drop from Excellent → Good even for very strong pseudocode.

**Recurring examples (appear across multiple pairs):**
- **P3/correct/Completeness** — LLM downgraded because student didn't write an explicit `print` statement at the end, even though the algorithm is fully described. Human: Excellent, LLM: Good.
- **P4/correct/Completeness** — LLM downgraded because student wrote "the function takes two numbers" instead of "FUNCTION calculation(a, b)". Human: Excellent, LLM: Good.
- **P5/correct/Clarity** — LLM downgraded informal language ("gives back 0") even though the recursive algorithm is described perfectly. Human: Excellent, LLM: Good.
- **P2/correct/Efficiency** — LLM penalized because checking membership in an output list implies O(N²) scanning. However, for beginner pseudocode, this is the most natural correct approach and does not mean the student doesn't understand efficiency.
- **P1/partially_correct/Efficiency** — LLM gave Fair because the student described N=5 steps without a formal loop, even though no inefficiency was demonstrated.

**Key insight:** Rubric prescription disproportionately hurts *correct* and *mostly correct* submissions. These students have the right understanding but get penalized for not using formal syntax the rubric demands.

---

### 🟠 2. Dimension Confusion (13 cases, 12%)

These are cases where the LLM identified a real problem but charged it to the wrong dimension.

**The most consistent pattern:** Penalizing **Efficiency** for what is actually a **Correctness** failure.

| Case | What the LLM said | What it really is |
|---|---|---|
| P2/partial/Efficiency | "Only handles adjacent duplicates — inefficient" | A **Correctness** flaw (wrong algorithm scope) |
| P3/partial/Efficiency | "Consonant formula is inefficient" | A **Correctness** flaw (wrong formula) |
| P4/incorrect/Efficiency | "Doesn't attempt the required calculations" | A **Correctness** flaw (wrong operation) |
| P5/largely_incorrect/Efficiency | "Infinite recursion is inefficient" | A **Correctness** flaw (no base case, algorithm never terminates) |
| P2/correct/Efficiency | "O(N²) scanning" | Debatable — this is an **Efficiency** concern but presupposes an implementation detail not stated in the pseudocode |

**Key insight:** The LLM has difficulty separating "this algorithm is wrong" from "this algorithm is inefficient." When an algorithm fails to solve the problem, the LLM sometimes awards a Poor on Efficiency instead of Correctness, leaving Correctness under-penalized or misdirecting the student's attention.

---

### 🟢 3. Legitimate Disagreement (58 cases, 55%)

The majority of disagreements — 55% — are cases where both the human and LLM have defensible positions. These reflect genuine evaluative ambiguity in the rubric.

**Three main sub-types of legitimate disagreement:**

**3a — Implicit vs. explicit requirements**
Many disagreements boil down to whether implied components count. E.g., does "I go through the numbers 1 to N" imply a proper loop? Does starting with answer=1 imply handling of N=0? Humans tend to credit implied understanding; the LLM requires explicit statement.

**3b — Partially correct algorithms**
How much credit for an algorithm that works for the specific example but fails generally?
- P1/partial/Correctness: Multiplies 5×4×3×2 but doesn't generalize → Good (human) vs. Fair (LLM)
- P2/partial/Correctness: Correctly handles adjacent duplicates but acknowledges failure for others → Fair (human) vs. Poor (LLM)

**3c — Clarity: surface readability vs. algorithmic precision**
The most consistently ambiguous dimension. Humans often rated clarity based on whether they could understand the student's intention. The LLM rated based on whether the pseudocode specifies an unambiguous algorithm with named variables and defined steps.
- "I count every character in the sentence" → Fair (human, understandable) vs. Poor (LLM, too vague algorithmically)

---

### 🔴 4. Human Error (23 cases, 22%)

These are the clearest-cut cases where the human gave a score that cannot be defended against the rubric.

**The human errors cluster almost entirely around `incorrect` and `largely_incorrect` submissions, and specifically in Correctness and Completeness.**

**Most egregious human errors (appear across all 4 pairs):**

| Problem/Level | Dimension | Human | LLM | Why it's a human error |
|---|---|---|---|---|
| P1/incorrect | Correctness | Fair | Poor | Student hardcoded 120 for inputs >5. Zero factorial logic present. |
| P2/largely_incorrect | Correctness | Good | Poor | Student's own pseudocode says "the order may be changed" — admits violating a core requirement |
| P2/incorrect | Correctness | Fair | Poor | Student removes ALL duplicated numbers instead of keeping first occurrence — fundamentally wrong problem |
| P4/incorrect | Correctness | Fair | Poor | Student multiplies instead of adds/subtracts — completely wrong operation |
| P4/incorrect | Completeness | Good | Poor | No function defined, no correct operations, no return statement — 0 of 5 sub-criteria met |

**Key insight:** The human rater appears to have applied a "student effort" bonus — giving partial credit for submissions that show some reasoning even when the core logic is completely wrong. While sympathetic, this inflates scores and misrepresents student competency.

---

### ⚫ 5. LLM Hallucination (2 cases, 2%)

Only 2 cases found, both in **rater1 vs OpenAI**:

**Case 1 — P2/incorrect/Efficiency (OpenAI):**
- OpenAI scored Efficiency as **Poor** with reason: *"Insufficient algorithmic detail to assess efficiency."*
- Reality: The student clearly described a frequency-counting approach (count occurrences, then filter), which is an O(N) strategy. There IS sufficient detail. The student's algorithm is wrong (removes all duplicates instead of keeping first), but that's a Correctness issue, not an Efficiency gap. The "insufficient detail" claim is a boilerplate fallback that doesn't reflect the actual pseudocode.

**Case 2 — P4/largely_incorrect/Efficiency (OpenAI):**
- OpenAI scored Efficiency as **Poor** with reason: *"Insufficient algorithmic detail to assess efficiency."*
- Reality: The student described exactly 2 operations (add, then subtract). This is perfectly detailed and not redundant. The LLM defaulted to a generic failure message rather than actually evaluating the efficiency of the described approach.

**Key insight:** LLM hallucination is rare (2%) and appears to be a specific pattern — OpenAI's fallback phrase "Insufficient algorithmic detail" is being applied incorrectly to submissions that do describe an algorithmic approach. Gemini never produced this type of response.

---

## Pattern Summary by Dimension

| Dimension | Most common disagreement cause |
|---|---|
| **Correctness** | Human error (over-crediting wrong logic) + Legitimate disagreement |
| **Completeness** | Rubric prescription (explicit output/function keyword required) + Legitimate disagreement |
| **Clarity** | Legitimate disagreement (natural language vs. algorithmic precision) |
| **Efficiency** | Dimension confusion (Correctness flaws charged to Efficiency) + Legitimate disagreement |

---

## Pattern Summary by Student Level

| Student level | Most common disagreement cause |
|---|---|
| **Correct** | Rubric prescription (LLM too strict on well-done submissions) |
| **Partially correct** | Legitimate disagreement (how much credit for partial logic?) |
| **Largely incorrect** | Legitimate disagreement + Human error |
| **Incorrect** | Human error (human too lenient) + Dimension confusion |

---

## Recommendations Based on This Analysis

| Priority | Recommendation | Fixes |
|---|---|---|
| **High** | Revise rubric sub-criteria to avoid requiring formal syntax (e.g., FUNCTION keyword, explicit print) for pseudocode | Reduces Rubric prescription cases |
| **High** | Add calibration examples to the rubric for what "partial credit" means at each level | Reduces Human error + Legitimate disagreement |
| **Medium** | Strengthen evaluator prompt rule: "Penalize Efficiency only for algorithmic inefficiency (redundant loops, unnecessary passes). Never penalize Efficiency because the algorithm is wrong." | Reduces Dimension confusion |
| **Medium** | Add a Clarity rubric note: "Natural-language descriptions that clearly convey the algorithm's intent are acceptable. Informality alone does not reduce Clarity." | Reduces Rubric prescription for Clarity |
| **Low** | Replace OpenAI's boilerplate "Insufficient detail" Efficiency fallback with a rule to give Fair instead of Poor when the approach is described but incomplete | Eliminates LLM hallucination pattern |
