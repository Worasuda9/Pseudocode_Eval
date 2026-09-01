# FILE: 10_version_explanations.txt
# DESCRIPTION: Explanation and rationale for each prompt version (V1 through V4.3)
# SOURCE: version_explanations.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Every Prompt Version — Clear Explanation
## Reference guide for the final presentation

---

> **How to use this document:**
> Read this before your meeting. Each version is explained in the same structure:
> **What changed → Why we tried it → What happened → Why we moved on**

---

## Version Timeline

```
V1 → V2 → V3 → V_clarity20 → V4 → V3.5 → [new rubrics] → Gemini7 → V3.6 → V4 (new rubrics) ✅
                   ↑                  ↑
             Stable baseline    Best with old rubrics
                                  (but EFF fails)
```

---

## V1 — The First Version
**Status: Historical (not in final report)**

### What it was
The very first evaluation prompt. Basic instructions to score pseudocode on four dimensions. No special rules, no calibration examples, no FIX blocks.

### What happened
Agreement was poor. The model confused dimensions — for example, penalizing Efficiency because the algorithm was wrong (dimension confusion), or giving Poor Clarity just because the logic was incorrect.

### Why we moved on
Needed structured rules to prevent specific evaluation bugs.

---

## V2 / V3 / V_clarity18 — Iterative Improvements
**Status: Historical (not in final report)**

### What changed across these versions
Each iteration added more targeted rules:
- V2: Added basic dimension separation rules
- V3: Added the five `[FIX: ...]` rule blocks for specific bugs
- V_clarity18: Refined Clarity rules (18 refers to a specific rule count)

### What happened
Agreement improved with each version. The five FIX rules were effective at preventing the most common bugs.

### Why we moved on
V_clarity20 was the refined, cleaner version of this line.

---

## V_clarity20 — The Stable Baseline ⭐
**Status: Previous best. Used as the comparison point for all later experiments.**

| Dimension | κ | Interpretation |
|---|---|---|
| Correctness | 0.754 | Substantial |
| Completeness | 0.786 | Substantial |
| Clarity | **0.631** | **Substantial** ← best Clarity ever |
| Efficiency | 0.625 | Substantial |
| **Weighted κ** | **0.726** | **Substantial** |

### What it was
A prompt with **lenient tier anchors** (forgiving of edge cases and informal wording) AND all **five FIX rules** to protect against dimension confusion, Clarity hallucination, and absence penalization.

**Lenient tier example (Correctness Excellent):**
> *"Core algorithm logic is sound for typical inputs. Minor edge cases or informal wording do not affect this score."*

**Five FIX rules present:**
1. FIX: Dimension confusion — Efficiency
2. FIX: Absence penalization
3. FIX: Clarity independence from correctness
4. FIX: Clarity hedging ceiling
5. FIX: Completeness implied output

### Why we tried to improve it
Correctness was only 0.754 — the lowest weighted dimension. We believed stricter tier anchors could push it higher. We also wanted to understand if GPT-4o-mini could use the same prompt.

---

## V4 — Strict Tier Anchors, No FIX Rules
**Status: Tested with old rubrics. EFF failed the threshold.**

| Dimension | κ (old rubrics) | Interpretation |
|---|---|---|
| Correctness | 0.822 | Almost Perfect ✅ |
| Completeness | **0.887** | Almost Perfect ✅ |
| Clarity | 0.533 | Moderate ⚠️ |
| Efficiency | 0.585 | **Moderate ❌ (below threshold)** |
| **Weighted κ** | **0.760** | **Substantial** |

### What changed from V_clarity20
Replaced ALL tier anchors with strict versions AND removed all five FIX rules.

**Strict tier example (Correctness Excellent):**
> *"Algorithm produces perfectly correct results for ALL valid inputs and edge cases."*

**Strict tier example (Completeness Excellent):**
> *"Every structural component and edge case explicitly defined in the rubric is present."*

### Why we tried it
V_clarity20's "Minor edge cases do not affect this score" was too lenient. We thought a stricter bar would push Correctness and Completeness up — and it did. Both reached Almost Perfect.

### What happened
Correctness jumped from 0.754 → 0.822 ✅. Completeness was 0.887 (best ever) ✅. But Clarity dropped from 0.631 → 0.533 (Moderate) ⚠️. And Efficiency was 0.585 — **below the Substantial threshold of 0.61** ❌.

### Why we moved on
Efficiency failing the Substantial threshold disqualified V4 as a production version. Also, this was tested only on old rubrics (which had a structural error — edge cases under the wrong dimension). We needed to fix the rubrics first.

---

## V3.5 — The Combination Attempt (V4 Tiers + V_clarity20 FIX Rules)
**Status: Failed. This was tested this week.**

| Dimension | κ (old rubrics) | Interpretation |
|---|---|---|
| Correctness | 0.753 | Substantial |
| Completeness | 0.816 | Almost Perfect |
| Clarity | 0.503 | Moderate ❌ |
| Efficiency | 0.498 | **Moderate ❌** |
| **Weighted κ** | **0.697** | Worse than V_clarity20 |

### What changed from V4
Kept V4's strict tier anchors AND added back all five FIX rules from V_clarity20. The idea was to get the best of both worlds.

### Why we tried it
**Hypothesis:** V4 proved strict tiers improve Correctness and Completeness. V_clarity20 proved FIX rules protect Clarity and Efficiency. If both are true independently, combining them should give the best of both worlds.

### What happened
It did not work. Correctness barely moved (0.753 vs V_clarity20's 0.754 — almost identical). Clarity dropped further to 0.503. Efficiency dropped to 0.498. Weighted κ fell to 0.697.

### Why it failed
V4's strict Clarity tier anchor ("No ambiguity whatsoever") was so demanding that even the FIX rules could not protect Clarity scores from being pulled down. The FIX rules tell the model *what to protect*, but the tier anchor overrides the scoring floor. The strict anchor and the lenient FIX rules contradicted each other.

### Why we moved on
Failed on both Clarity and Efficiency. V_clarity20 remained the best at this point.

---

## Rubric Generator Fix — Critical Structural Change
**Status: Applied before all further experiments. This is not a prompt version — it is a rubric fix.**

### What the problem was
The old rubric for problem 1 (factorial) had this under **Correctness:**
> *"The logic correctly handles the base case for an input of 0 or 1."*

Edge cases (like N=0) belong under **Completeness**, not Correctness. Correctness should only evaluate whether the core algorithm logic is mathematically sound. An edge case is about whether all required scenarios are covered — that is a structural completeness question, not a correctness question.

### Why this mattered
GPT-4o-mini followed this rubric exactly and penalized Correctness for a missing edge case. Gemini used its thinking mode to reason around the bad rubric. So GPT looked like it was over-penalizing — but it was actually correct to follow the rubric. The rubric was wrong.

### What we fixed
Added an explicit rule to the rubric generator:
> *"Edge cases belong under Completeness ONLY. Do not list edge cases under Correctness."*

Then regenerated all 10 problem rubrics with the improved generator.

### Effect
This was the single biggest driver of Correctness improvement. Correctness jumped from 0.754 (old rubrics) → 0.822–0.864 (new rubrics) across subsequent versions.

---

## Gemini7 — All 6 Consistency Fixes (New Rubrics)
**Status: Failed on Clarity. Tested this week.**

| Dimension | κ (new rubrics) | Interpretation |
|---|---|---|
| Correctness | 0.822 | Almost Perfect ✅ |
| Completeness | 0.783 | Substantial ✅ |
| Clarity | **0.297** | **Fair ❌ — worst ever** |
| Efficiency | 0.662 | Substantial ✅ |
| **Weighted κ** | **0.689** | Worse than V_clarity20 |

### What changed
Applied 6 consistency fixes to V_clarity20 AND used new corrected rubrics:
1. Removed outdated weights (40/30/20/10)
2. Extended hints to Good/Fair/Poor (not just Fair/Poor)
3. Added edge case ownership rule to evaluator
4. Merged duplicate Completeness rules
5. Added bridging sentence in Clarity tier
6. Merged two duplicate Clarity FIX blocks into one

### Why we tried it
After fixing the rubric generator, we wanted to clean up all remaining inconsistencies in the evaluation prompt. The 6 fixes were logically correct improvements.

### What happened
Correctness jumped to 0.822 ✅. But Clarity crashed from 0.631 → 0.297 ❌ — the worst we have ever seen.

### Why Clarity crashed
The merged Clarity block repeatedly emphasized *"wrong logic does NOT lower Clarity"*. The model over-applied this principle and gave Excellent Clarity to nearly all submissions, even ones where the writing itself was vague or fragmented.

Interestingly, we found that some of the Clarity disagreement was actually **Human Error** — the human raters let wrong logic influence their Clarity score. But the model went too far in the other direction.

### Why we moved on
Clarity at 0.297 was unacceptable. Needed to add a boundary to the Clarity rule.

---

## V3.6 — Strict Clarity Tier Only (New Rubrics)
**Status: Partial success. Tested this week.**

| Dimension | κ (new rubrics) | Interpretation |
|---|---|---|
| Correctness | 0.823 | Almost Perfect ✅ |
| Completeness | 0.786 | Substantial ✅ |
| Clarity | 0.447 | Moderate ⚠️ |
| Efficiency | 0.662 | Substantial ✅ |
| **Weighted κ** | **0.720** | Close to V_clarity20 |

### What changed from Gemini7
Only the Clarity tier anchors were changed to V4's strict versions:
- Excellent: *"No ambiguity or vague language whatsoever"* (strict)
- Good: *"Some ambiguity requiring minor inference"* (tightened)

Everything else (Correctness, Completeness, Efficiency tiers, all FIX rules) remained at Gemini7 / V_clarity20 levels.

Also added a Clarity boundary rule:
> *"Clarity independence applies only when writing is readable but logic is wrong. If writing is ALSO vague or incomprehensible, score based on actual readability."*

### Why we tried it
The Clarity anchor was too lenient in Gemini7 — the model needed a stricter ceiling. But we did not want to disturb the other dimensions. So we changed only Clarity.

### What happened
Clarity recovered from 0.297 → 0.447 ✅ (big improvement). But still Moderate, not Substantial. Weighted κ was 0.720 — very close to V_clarity20's 0.726 but with Clarity still below target.

### Why we moved on
Still not optimal. V4 with new rubrics was the next candidate to test.

---

## V4 with New Rubrics — The Production Baseline ✅
**Status: WINNER. Current production prompt.**

| Test | Weighted κ | COR | COM | CLA | EFF |
|---|---|---|---|---|---|
| 5 problems (n=20) | **0.740** | 0.864 | 0.754 | 0.537 | 0.614 |
| 10 problems (n=40) | **0.684** | 0.850 | 0.646 | 0.494 | 0.513 |

### What changed from V3.6
Reverted to pure V4: strict tier anchors for ALL four dimensions AND removed all three remaining FIX rules:
- Removed: FIX Dimension confusion — Efficiency
- Removed: FIX Absence penalization
- Removed: FIX Clarity — independence from correctness

Combined with the new corrected rubrics (edge cases under Completeness).

### Why we tried it
V4 had the highest historical weighted κ (0.760) — but that was with old rubrics where EFF was 0.585 (failing). New rubrics correctly place edge cases under Completeness. We had never tested V4 against correct rubrics. The question was: does V4 pass EFF with new rubrics?

### What happened
**Yes** — EFF jumped from 0.585 (old rubrics) → 0.614 (new rubrics). Just above the Substantial threshold. Correctness reached 0.864 — the best ever. Clarity improved to 0.537. Weighted κ = 0.740 on 5 problems.

On 10 problems, overall κ dropped to 0.684 — expected from more diverse problems. EFF also dropped to 0.513 (Moderate) — this revealed that removing the Efficiency FIX rule hurts at scale.

### Why this is the production version
- Highest overall kappa with correct rubrics
- Correctness at Almost Perfect level
- EFF passes on 5 problems; needs FIX rule restored for 10+ problems
- Structurally correct rubrics (edge cases under Completeness)

### What is still to fix
Add back `[FIX: Dimension confusion — Efficiency]` to prevent EFF from dropping at scale. This is the **Friday July 17 task**.

---

## Quick Comparison: All Versions at a Glance

| Version | Key Change | Rubrics | COR | COM | CLA | EFF | κ | Pass? |
|---|---|---|---|---|---|---|---|---|
| V_clarity20 | Lenient tiers + 5 FIX rules | Old | 0.754 | 0.786 | **0.631** | 0.625 | 0.726 | ✅ All ≥ Substantial |
| V4 | Strict tiers, no FIX rules | Old | 0.822 | **0.887** | 0.533 | 0.585 | 0.760 | ❌ EFF fails |
| V3.5 | V4 tiers + FIX rules | Old | 0.753 | 0.816 | 0.503 | 0.498 | 0.697 | ❌ CLA+EFF fail |
| Gemini7 | 6 consistency fixes | New | 0.822 | 0.783 | 0.297 | 0.662 | 0.689 | ❌ CLA crash |
| V3.6 | Strict CLA tier only | New | 0.823 | 0.786 | 0.447 | 0.662 | 0.720 | ❌ CLA low |
| **V4 (new)** | **Pure V4 + correct rubrics** | **New** | **0.864** | 0.754 | 0.537 | 0.614 | **0.740** | ✅ Best overall |

---

## The One-Sentence Summary of Each Version

| Version | One sentence |
|---|---|
| V_clarity20 | Lenient and protective — good enough but Correctness was the weak point |
| V4 (old) | Strict and demanding — great on COR and COM but Efficiency failed |
| V3.5 | Tried to combine both — the strict tiers and lenient rules contradicted each other |
| Gemini7 | Fixed consistency issues but accidentally made Clarity too lenient (0.297) |
| V3.6 | Fixed Clarity partially — got it to 0.447 but not Substantial |
| **V4 (new)** | **The right prompt (V4) finally paired with correct rubrics — best overall result** |

---

## The Key Insight from All Experiments

> **The biggest improvement did not come from changing the prompt at all.**
> It came from fixing the **rubric generator** — moving edge cases from Correctness to Completeness.
> That single structural fix drove Correctness from 0.754 → 0.864, which is why V4 with new rubrics wins.
> The prompt engineering experiments were important for finding the right tier balance,
> but the rubric fix was the real breakthrough.
