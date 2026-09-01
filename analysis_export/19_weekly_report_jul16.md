# FILE: 19_weekly_report_jul16.txt
# DESCRIPTION: Weekly report July 10–16: prompt finalization + Gemini vs OpenAI comparison
# SOURCE: weekly_report_jul16.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Weekly Progress Report — July 10–16, 2026
## Pseudocode Evaluation System: Prompt Finalization & Provider Comparison

---

## Executive Summary

This week achieved two major milestones:
1. **Finalized the evaluation prompt** after a rigorous series of 6 prompt engineering experiments, landing on **V4 with new rubrics** as the production baseline (weighted κ = 0.740 on 5 problems, 0.684 on 10 problems)
2. **Completed the first Gemini vs OpenAI provider comparison** across 10 problems, conclusively showing **Gemini 2.5 Flash significantly outperforms GPT-4o-mini** on all four evaluation dimensions

---

## Background: Where We Started This Week

### Previous baseline: V_clarity20
Going into this week, the best prompt was **V_clarity20** — a prompt with lenient tier anchors and five targeted `[FIX: ...]` rule blocks designed to prevent specific evaluation bugs:
- κ = 0.726 (Substantial) on 5 problems
- All dimensions Substantial or above
- Known weakness: Correctness κ = 0.754 (lowest dimension, 40% weight)

### Outstanding questions entering the week
1. Can we improve Correctness without breaking Clarity or Efficiency?
2. Does GPT-4o-mini work with the same prompt?
3. What is the maximum achievable kappa with the current rubrics?

---

## Part 1: V3.5 Experiment — Can We Combine V4 and V_clarity20?

### What we tried
**V3.5** = Take V4's strict tier anchors for all four dimensions + keep all five of V_clarity20's targeted [FIX] rules.

**Hypothesis:** V4's strict tiers proved better for Correctness and Completeness. V_clarity20's FIX rules protected Clarity and Efficiency from the "Excellent means perfect" overcorrection. If both are true independently, combining them should give the best of both worlds.

### Results (5 problems, old rubrics)

| Dimension | V_clarity20 | V3.5 | Change |
|---|---|---|---|
| Correctness | 0.754 | 0.753 | ≈ same |
| Completeness | 0.786 | 0.816 | +0.030 ✅ |
| Clarity | **0.631** | 0.503 | −0.128 ❌ |
| Efficiency | 0.625 | 0.498 | −0.127 ❌ |
| Weighted κ | **0.726** | 0.697 | −0.029 |

### What went wrong and why
V4's "No ambiguity or vague language whatsoever" Excellent Clarity anchor was too strict, even with the FIX rules present. The FIX rules tell the model *what to protect*, but V4's tier anchor overrides the floor by setting such a high bar that most student submissions get downgraded. The strict Correctness anchor also didn't help — Correctness was already fine at 0.754.

### Conclusion
V3.5 failed. V_clarity20 remained the baseline going into the rest of the week.

---

## Part 2: Root Cause Analysis — Why GPT-4o-Mini Over-Penalizes

### What we investigated
We ran GPT-4o-mini on p001 (factorial problem) and found it graded significantly harsher than Gemini and human raters. Specifically:
- s001 (mostly correct): GPT gave Good on Correctness, Completeness, and Clarity — humans gave Excellent on all three
- s002 (partially correct): GPT gave **Poor** on Correctness, Completeness, and Efficiency — Gemini gave Fair/Good

### The root cause (critical finding)
After reading the actual traces, we discovered **GPT was correct to follow the rubric** — the problem was the rubric itself.

The p001 rubric had this sub-criterion placed under **Correctness**:
> *"The logic correctly handles the base case for an input of 0 or 1, ensuring the factorial is 1."*

Edge cases should go under **Completeness**, not Correctness. The rubric generator made this mistake. GPT faithfully penalized Correctness for a missing edge case, while Gemini used its thinking mode to reason around the bad rubric.

**Key insight:** GPT is not the problem. The rubric generator is the problem.

### Why this matters
This is a systemic issue — if the rubric generator keeps placing edge cases under Correctness, every future GPT evaluation will be biased. Fixing the rubric generator fixes the root cause for all future evaluations.

---

## Part 3: The 6 Consistency Fixes — Prompt Audit

### What we did
We performed a full consistency audit of `prompts.py` and found 4 inconsistencies plus 2 additional improvements. All 6 were applied.

| Fix | Problem | Solution |
|---|---|---|
| **1. Remove weights** | Default weights (40/30/20/10) were listed in the rubric generator instructions, but they're irrelevant for qualitative scoring. Leftover from the old numeric system. | Removed weight instructions; hardcoded values in JSON template only |
| **2. Hints for Good/Fair/Poor** | Hints were only required for Fair and Poor. Good scores got null hints, meaning students with minor gaps got no guidance. | Changed rule: hints required for Good, Fair, and Poor. Null only for Excellent. |
| **3. Edge case ownership in evaluator** | The edge case rule ("belongs under Completeness only") existed in the rubric generator but was missing from the evaluator. GPT had no evaluator-level override to stop it from following a wrong rubric. | Added explicit edge case ownership rule to evaluator: *"Edge cases belong under Completeness ONLY."* |
| **4. Unify absence penalization** | The implied-output rule existed in two separate FIX blocks with slightly different wording. Could cause inconsistent behavior. | Merged into single `[FIX: Absence penalization]` block |
| **5. Clarity bridging sentence** | The Clarity Excellent tier said "no hedging" but didn't connect to the hallucination prevention rule ("wrong logic ≠ unclear writing"). Potential contradiction. | Added bridging sentence: *"Wrong logic does not lower Clarity — only vagueness or ambiguity does."* |
| **6. Merge duplicate Clarity rules** | Two separate Clarity FIX blocks (hallucination prevention + hedging ceiling) said similar things in different sections. | Merged into one unified `[FIX: Clarity — independence from correctness and hedging ceiling]` |

---

## Part 4: Gemini7 Experiment — Did the Fixes Help or Hurt?

### What we tested
Applied all 6 fixes ("Gemini7") to new regenerated rubrics (rubrics were regenerated using the improved rubric generator, with edge cases now correctly under Completeness).

### Results (5 problems, new rubrics)

| Dimension | V_clarity20 | Gemini7 | Change |
|---|---|---|---|
| Correctness | 0.754 | 0.822 | +0.068 ✅ |
| Completeness | 0.786 | 0.783 | ≈ same |
| **Clarity** | 0.631 | **0.297** | **−0.334 🔴** |
| Efficiency | 0.625 | 0.662 | +0.037 ✅ |
| Weighted κ | **0.726** | **0.689** | −0.037 |

### Why Clarity crashed
The merged, more prominent Clarity block with repeated *"wrong logic does NOT lower Clarity"* caused Gemini to award Excellent/Good Clarity to nearly all submissions, including ones that were both logically wrong AND poorly written.

### Real-world verification
We read the actual p001 submissions (s3 and s4) to verify:
- **s3:** *"Take the number 5 and add all numbers before it together. So I add 5+4+3+2+1."* — The writing is crystal clear (addition instead of multiplication), wrong logic but readable → Excellent Clarity is **correct** under our rules. Human's Fair was **Human Error**.
- **s4:** *"I check if the number is bigger than 5. If it is, I print 120."* — Clearly stated conditions, just wrong logic → Good Clarity is **correct**. Human's Poor was **Human Error**.

**Key finding:** Some of the Clarity disagreement is genuine Human Error (raters penalizing clarity for wrong logic), not LLM over-leniency. However, Gemini was also too lenient in other cases.

### Clarity boundary fix applied
Added a critical new rule:
> *"IMPORTANT BOUNDARY: Clarity independence applies only when the writing itself is readable but the logic happens to be wrong. If the writing is ALSO vague, fragmented, or incomprehensible — score Clarity based on actual readability, not on the assumption that all wrong answers must be well-written."*

Also added concrete calibration examples anchoring the Poor end of the Clarity scale.

---

## Part 5: Prompt Finalization — Finding the Production Baseline

After the Gemini7 crash, we ran three more targeted experiments to find the optimal configuration with new rubrics.

### Experiment A: V3.6 — Strict Clarity Tier Only
Only the Clarity Excellent and Good tier anchors were changed to V4's strict versions. All other tiers (Correctness, Completeness, Efficiency) kept at V_clarity20's lenient levels. All FIX rules kept.

| Dimension | Gemini7 | V3.6 | Change |
|---|---|---|---|
| Correctness | 0.822 | 0.823 | ≈ same |
| Completeness | 0.783 | 0.786 | ≈ same |
| Clarity | 0.297 | **0.447** | +0.150 ✅ |
| Efficiency | 0.662 | 0.662 | 0.000 |
| Weighted κ | 0.689 | **0.720** | +0.031 |

**Result:** Clarity recovered significantly. But still Moderate (need ≥ 0.61 for Substantial). Weighted κ = 0.720, close to V_clarity20's 0.726.

### Experiment B: V4 with New Rubrics (pure V4, no FIX rules)
Reverted to pure V4: strict tier anchors for ALL 4 dimensions AND removed all three [FIX: ...] evaluator blocks. This was a fair test of V4 with new corrected rubrics for the first time.

| Dimension | V3.6 | V4 (new) | Change |
|---|---|---|---|
| Correctness | 0.823 | **0.864** | +0.041 ✅ |
| Completeness | 0.786 | 0.754 | −0.032 |
| Clarity | 0.447 | **0.537** | +0.090 ✅ |
| Efficiency | 0.662 | 0.614 | −0.048 ⚠️ |
| **Weighted κ** | 0.720 | **0.740** | **+0.020** |

**Result:** V4 with new rubrics is the winner — highest weighted κ = 0.740, best Correctness ever (0.864), Clarity improved to 0.537. Efficiency barely above Substantial (0.614).

### Why new rubrics changed V4's Efficiency weakness
V4 with OLD rubrics had EFF = 0.585 (below Substantial). V4 with NEW rubrics has EFF = 0.614 (Substantial). The new rubrics correctly separate edge cases into Completeness — this means the model no longer has to handle edge cases in Efficiency evaluation, reducing confusion.

### The Clarity practical ceiling
Across all new-rubric experiments, Clarity improved as the tier anchor tightened:

| Version | Clarity κ |
|---|---|
| Gemini7 (lenient FIX rules dominant) | 0.297 |
| V3.6 (strict Clarity Excellent tier only) | 0.447 |
| V4 (strict all tiers, no FIX rules) | **0.537** |

The ceiling appears to be ~0.54 with new rubrics. The new Clarity sub-criteria are more algorithmically specific, creating structural disagreement with human raters who evaluate holistically. This is not a prompt problem — it is a fundamental property of the new rubrics.

**Decision: Lock V4 with new rubrics as the production baseline.**

---

## Part 6: Full Comparison Summary — All Prompt Versions

| Version | Rubrics | COR | COM | CLA | EFF | Weighted κ | Status |
|---|---|---|---|---|---|---|---|
| V_clarity20 | Old | 0.754 | 0.786 | 0.631 | 0.625 | 0.726 | Old baseline |
| V3.5 | Old | 0.753 | 0.816 | 0.503 | 0.498 | 0.697 | ❌ Failed |
| V4 | Old | 0.822 | 0.887 | 0.533 | 0.585 | 0.760 | EFF fails |
| Gemini7 fixed | New | 0.822 | 0.783 | 0.297 | 0.662 | 0.689 | ❌ CLA crash |
| V3.6 | New | 0.823 | 0.786 | 0.447 | 0.662 | 0.720 | CLA low |
| **V4 (new rubrics)** | **New** | **0.864** | **0.754** | **0.537** | **0.614** | **0.740** | ✅ **PRODUCTION** |

---

## Part 7: Gemini vs OpenAI — 10-Problem Evaluation

### Setup
- 10 problems × 4 submissions = 40 evaluations per provider
- New corrected rubrics for all 10 problems
- Same V4 production prompt for both providers
- Compared against 2 human raters (n=40 each)

### Human Inter-Rater Agreement (Ground Truth)

| Dimension | κ | Agreement % |
|---|---|---|
| Correctness | 0.899 | 87.5% |
| Completeness | 0.878 | 85.0% |
| Clarity | 0.817 | 80.0% |
| Efficiency | 0.919 | 92.5% |

All Almost Perfect — validates rubric quality and confirms reliable ground truth.

### Gemini 2.5 Flash Results

| Dimension | Avg κ | Interpretation |
|---|---|---|
| Correctness | **0.850** | Almost Perfect ✅ |
| Completeness | **0.646** | Substantial ✅ |
| Clarity | 0.494 | Moderate ⚠️ |
| Efficiency | 0.513 | Moderate ⚠️ |
| **Weighted κ** | **0.684** | **Substantial** |

### GPT-4o-mini Results

| Dimension | Avg κ | Interpretation |
|---|---|---|
| Correctness | 0.632 | Substantial ✅ |
| Completeness | 0.521 | Moderate ⚠️ |
| Clarity | 0.306 | Fair ❌ |
| Efficiency | 0.367 | Fair ❌ |
| **Weighted κ** | **0.507** | **Moderate** |

### Head-to-Head Comparison

| Dimension | Human κ | Gemini κ | OpenAI κ | Gemini Gap | OpenAI Gap |
|---|---|---|---|---|---|
| Correctness (40%) | 0.899 | **0.850** | 0.632 | 0.049 | 0.267 |
| Completeness (30%) | 0.878 | **0.646** | 0.521 | 0.232 | 0.357 |
| Clarity (20%) | 0.817 | **0.494** | 0.306 | 0.323 | 0.511 |
| Efficiency (10%) | 0.919 | **0.513** | 0.367 | 0.406 | 0.552 |
| **Weighted κ** | ~0.880 | **0.684** | **0.507** | **0.196** | **0.373** |

**Gemini wins on every single dimension.** Gemini's gap to human agreement (0.196) is less than half of OpenAI's gap (0.373).

---

## Key Findings and Their Meaning

### Finding 1: Gemini is the right model for this task
Weighted κ = 0.684 (Substantial) vs OpenAI's 0.507 (Moderate). Gemini's thinking mode allows it to reason through complex multi-rule prompts, apply contextual judgment, and avoid dimension confusion. GPT-4o-mini applies rules as a checklist without contextual reasoning.

### Finding 2: Correctness is solved
Gemini κ = 0.850 on Correctness, just 0.049 below human agreement. The improved rubrics (edge cases under Completeness) are the primary driver. The system can reliably identify correct vs incorrect algorithmic logic.

### Finding 3: Clarity and Efficiency remain the hardest dimensions
For Gemini: CLA=0.494, EFF=0.513 (both Moderate). These dimensions require holistic human judgment that current LLMs cannot fully replicate:
- **Clarity:** Humans integrate logic quality into their readability judgment; LLMs are trained to separate them
- **Efficiency:** Requires understanding algorithmic intent and performance trade-offs at a conceptual level

### Finding 4: Removing the Efficiency FIX rule hurt at scale
On 5 problems, EFF=0.614 (just Substantial). On 10 problems, EFF=0.513 (Moderate). The `[FIX: Dimension confusion — Efficiency]` rule was removed in V4 to achieve pure V4 behavior. At scale, this led the model to confuse Efficiency with Correctness on more complex problems. This is the clearest actionable next step.

### Finding 5: OpenAI has a systematic Clarity bias
GPT-4o-mini κ = 0.306 on Clarity with only 32.5% exact agreement. This is not random — GPT systematically conflates logical correctness with clarity, penalizing clear-but-wrong answers and rewarding correct-but-vague answers. The FIX rules that protect against this require extended reasoning capabilities that GPT-4o-mini lacks.

### Finding 6: Human error is a real factor (11% of disagreements)
From earlier analysis, approximately 11% of Human vs LLM disagreements are actually cases where the LLM is correct and the human rater made an error (confirmed on p001 s3/s4: humans penalized Clarity for wrong logic, which our rules explicitly prohibit). The "true" LLM performance is slightly better than raw kappa suggests.

---

## Rubric Quality Improvement

A critical structural improvement was also made this week: **all 10 problem rubrics were regenerated** using an improved rubric generator prompt. The key change:

**Before:** Edge cases (e.g. N=0, empty input) could appear under Correctness as sub-criteria, causing double-penalization when a student wrote correct logic but didn't mention the edge case.

**After:** Edge cases belong under Completeness ONLY, stated explicitly twice in the rubric generator prompt. This was the single biggest driver of the Correctness improvement (0.754 → 0.864).

---

## Next Steps

| Priority | Action | Rationale |
|---|---|---|
| 🔴 High | Reintroduce `[FIX: Dimension confusion — Efficiency]` rule | EFF dropped from 0.614 (5 problems) to 0.513 (10 problems) at scale — the FIX rule is needed |
| 🟡 Medium | Regenerate rubrics for remaining 5 problems (p11–p15) | Currently validated on 10/15 problems |
| 🟡 Medium | Run full 15-problem evaluation with Gemini | Confirm production baseline at scale |
| 🟢 Low | Test OpenAI with FIX rules added back | May significantly improve OpenAI Clarity/Efficiency without major changes to Correctness |
| 🟢 Low | Investigate Completeness at scale | COM dropped from 0.754 (5 problems) to 0.646 (10 problems) — may need attention |
