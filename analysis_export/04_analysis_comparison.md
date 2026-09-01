# FILE: 04_analysis_comparison.txt
# DESCRIPTION: Comparative analysis across evaluation versions
# SOURCE: analysis_comparison.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Analysis Comparison: Yours vs. Mine
## Which disagreement categorization is more correct?

---

## Side-by-Side: Total Counts

| | Your analysis | My analysis |
|---|---|---|
| **R1 vs Gemini** | 33 | 31 |
| **R1 vs OpenAI** | 29 | 27 |
| **R2 vs Gemini** | 32 | 28 |
| **R2 vs OpenAI** | 38 | 28 |
| **Grand total** | **132** | **114** |

> Your analysis found **18 more disagreements** overall. The biggest gap is in R2 vs OpenAI (38 vs 28). This means my subagents missed some cases when comparing the CSVs — most likely in the **Completeness dimension**, where your analysis includes more rows (e.g. P1/correct/COM, P2/correct/COM, P2/partially_correct/COM, P1/largely_incorrect/COM, P1/incorrect/COM).

---

## Category Framework Comparison

| Your category | My category | Same concept? |
|---|---|---|
| A — LLM systematic strictness (69%) | "Human error" + "Legitimate disagreement" | ❌ Major difference |
| B — Absence penalization (1%) | (no equivalent) | ❌ Missing from mine |
| C — Rubric prescription (12%) | Rubric prescription (17%) | ✅ Same |
| D — Dimension confusion (0%!) | Dimension confusion (12%) | ❌ Major difference |
| E — Legitimate disagreement (0%!) | Legitimate disagreement (55%) | ❌ Major difference |
| F — LLM leniency (12%) | (no equivalent — I split into "Human error" or "Legitimate") | ❌ Missing from mine |
| G — LLM hallucination (4%) | LLM hallucination (2%) | ✅ Similar |

---

## Where Your Analysis Is More Correct

### 1. ✅ Total disagreement count is higher and more complete
Your analysis found 132 disagreements vs. my 114. The gap is real — my subagents missed cases in Completeness (especially R2 vs OpenAI), which your analysis covers. **Your counts are more accurate.**

### 2. ✅ "LLM systematic strictness" (A) is a better primary category than "Legitimate disagreement"
My framework labeled 55% of cases as "Legitimate disagreement" — implying both sides are equally defensible. Your framework correctly identifies that **69% of cases are A: the LLM is consistently scoring lower (stricter) than the human**. This is not neutral; it is a directional bias. Calling it "LLM systematic strictness" is more honest about what is actually happening.

For example, in P3/largely_incorrect/Clarity: I said "Legitimate disagreement" (both sides defensible). But looking at all 4 pairs, the LLM consistently gave Poor to the human's Fair on this exact case. That consistency is evidence of **systematic strictness**, not random legitimate disagreement.

### 3. ✅ "LLM leniency" (F) is a valid and necessary category
I had no "LLM leniency" category. Cases like P4/partially_correct/EFF (Fair vs Excellent) I labeled either "Human error" or "Legitimate disagreement." Your framework correctly identifies these as **the LLM being too lenient** — not the human being wrong. This is the right framing for these cases.

### 4. ✅ LLM hallucination count is higher and more accurate (6 vs 2)
My subagents only flagged 2 hallucinations (both OpenAI/Efficiency). Your analysis correctly identifies **6 hallucinations**, including:
- P1/incorrect/CLA (R1 & R2 vs Gemini): Gemini gave **Excellent** clarity to a hardcoded wrong answer — a gap of 3 levels from the human's Poor. This is clearly a hallucination, not legitimate disagreement.
- P4/partially_correct/EFF and P4/largely_incorrect/EFF (R1 & R2 vs Gemini): Gemini gave **Excellent** efficiency to incomplete/wrong functions. My subagents called these "Legitimate disagreement" — which was wrong. No efficiency justification supports Excellent here.

---

## Where My Analysis Is More Correct (or Adds Value)

### 1. ⚠️ "Dimension confusion" is a real phenomenon your analysis dropped
Your framework has **D = Dimension confusion at 0%** — you didn't use this category at all. But dimension confusion is real and well-evidenced:
- P2/partially_correct/EFF: The LLM gave Poor for Efficiency because the algorithm "only handles adjacent duplicates." But that is a **Correctness** flaw (wrong scope), not an Efficiency flaw. A one-pass adjacent comparison is O(N) — efficient.
- P5/largely_incorrect/EFF: Infinite recursion penalized under Efficiency — but infinite recursion is a **Correctness** failure (no base case, never terminates), not an efficiency concern.
- P3/partially_correct/EFF: Penalizing Efficiency because the consonant formula is wrong — again a **Correctness** issue charged to Efficiency.

Your framework absorbed these into **A (LLM systematic strictness)**, which loses the information that the LLM is penalizing the *wrong dimension*, not just being stricter.

### 2. ⚠️ "Human error" is a real and important finding
I identified cases where the human clearly made a mistake:
- P2/largely_incorrect/COR: Human gave **Good** to an algorithm the student themselves admitted destroys order. Your analysis labels this **C (Rubric prescription)** — but this is not a rubric issue; ANY evaluator should know that an algorithm violating order-preservation is incorrect. The human rater was wrong here.
- P4/incorrect/COM: Human gave **Good** when the student had no function definition, wrong operation, and no return statement (0/5 sub-criteria). Your analysis labels this **A (LLM systematic strictness)** — but the LLM's Poor is correct and the human's Good is a clear error.

Not acknowledging human error misleads future calibration — if you correct the LLM to match the human here, you would be making the LLM less accurate.

### 3. ⚠️ My "Rubric prescription" overlap with your "A" 
Your analysis sometimes labels cases as A (LLM systematic strictness) that are actually caused by specific rubric wording. Example: P3/correct/COM — Gemini deducted because the student didn't write an explicit print/output statement. This isn't general LLM strictness; it's caused by the rubric sub-criterion "Outputs the final calculated vowel and consonant counts upon completion." Calling it A loses the root cause (fixable by changing the rubric).

---

## Verdict: Which Is More Correct?

| Dimension | Winner |
|---|---|
| **Total disagreement count** | ✅ **Yours** (132 vs 114 — yours is more complete) |
| **Primary bias direction** | ✅ **Yours** (A = systematic strictness is the right framing for 69% of cases) |
| **LLM leniency tracking** | ✅ **Yours** (F category is missing from mine) |
| **LLM hallucination detection** | ✅ **Yours** (6 vs 2 — yours caught the P4 Efficiency Excellent cases) |
| **Dimension confusion tracking** | ✅ **Mine** (D = 0% in yours is a gap — it IS happening) |
| **Human error identification** | ✅ **Mine** (your framework doesn't distinguish when the human was wrong) |
| **Root cause for rubric cases** | ✅ **Mine** (yours sometimes labels rubric-caused issues as generic A) |

**Overall: Your analysis is more correct on the big picture.**
The most important finding — that **69% of disagreements are the LLM being systematically stricter than humans (not random, not legitimate)** — is clearer and more actionable in your framework. Your total count is also more complete.

**My analysis adds value on two specific points:**
1. Dimension confusion is real and should not be collapsed into general strictness
2. Some "human error" cases exist where matching the LLM to the human would make it less accurate

---

## What Should Be Retained From Both

A combined framework would look like:

| Category | Source | Keep? |
|---|---|---|
| A — LLM systematic strictness | Yours | ✅ Yes — the dominant pattern |
| B — Absence penalization | Yours | ✅ Yes — useful sub-type of A |
| C — Rubric prescription | Both | ✅ Yes — specific fixable cause |
| D — Dimension confusion | Mine | ✅ Yes — real and distinct from A |
| F — LLM leniency | Yours | ✅ Yes — necessary counterpart to A |
| G — LLM hallucination | Both | ✅ Yes |
| Human error | Mine | ⚠️ Useful but politically sensitive to include |
| Legitimate disagreement | Mine | ❌ Too vague — replace with A or F |
