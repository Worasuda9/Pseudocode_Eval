# FILE: 12_evaluation_analysis_jul16.txt
# DESCRIPTION: Deep evaluation analysis from July 16 (Gemini vs OpenAI, 10 problems)
# SOURCE: evaluation_analysis_jul16.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# 10-Problem Evaluation Analysis — Gemini vs OpenAI
## July 16, 2026 — Weekly Meeting Report

---

## Human Inter-Rater Agreement (Ground Truth Baseline)

| Dimension | κ (R1 vs R2) | Agreement % | Interpretation |
|---|---|---|---|
| Correctness | 0.899 | 87.5% | Almost Perfect |
| Completeness | 0.878 | 85.0% | Almost Perfect |
| Clarity | 0.817 | 80.0% | Almost Perfect |
| Efficiency | 0.919 | 92.5% | Almost Perfect |

> **Key point:** All four dimensions show Almost Perfect human agreement. This validates the rubric quality and confirms the ground truth is reliable. The task is well-defined.

---

## Full Results: LLM vs Human Raters

### Gemini 2.5 Flash

| Dimension | R1 vs Gemini | R2 vs Gemini | **Average κ** | Interpretation |
|---|---|---|---|---|
| Correctness | 0.841 | 0.858 | **0.850** | Almost Perfect ✅ |
| Completeness | 0.598 | 0.694 | **0.646** | Substantial ✅ |
| Clarity | 0.492 | 0.496 | **0.494** | Moderate ⚠️ |
| Efficiency | 0.494 | 0.532 | **0.513** | Moderate ⚠️ |
| **Weighted κ** | — | — | **0.684** | **Substantial** |

### GPT-4o-mini (OpenAI)

| Dimension | R1 vs OpenAI | R2 vs OpenAI | **Average κ** | Interpretation |
|---|---|---|---|---|
| Correctness | 0.628 | 0.636 | **0.632** | Substantial ✅ |
| Completeness | 0.580 | 0.461 | **0.521** | Moderate ⚠️ |
| Clarity | 0.311 | 0.301 | **0.306** | Fair ❌ |
| Efficiency | 0.366 | 0.368 | **0.367** | Fair ❌ |
| **Weighted κ** | — | — | **0.507** | **Moderate** |

### Gemini vs OpenAI (Self-Agreement)

| Dimension | κ | Interpretation |
|---|---|---|
| Correctness | 0.658 | Substantial |
| Completeness | 0.418 | Moderate |
| Clarity | 0.321 | Fair |
| Efficiency | 0.494 | Moderate |

> The low Gemini vs OpenAI agreement (especially Clarity = 0.321) shows the two models are making **different types of errors** — they are not converging on the same evaluation strategy.

---

## Head-to-Head Summary

| Dimension | Human κ | Gemini κ | OpenAI κ | Winner |
|---|---|---|---|---|
| Correctness (40%) | 0.899 | **0.850** | 0.632 | 🟢 Gemini (+0.218) |
| Completeness (30%) | 0.878 | **0.646** | 0.521 | 🟢 Gemini (+0.125) |
| Clarity (20%) | 0.817 | **0.494** | 0.306 | 🟢 Gemini (+0.188) |
| Efficiency (10%) | 0.919 | **0.513** | 0.367 | 🟢 Gemini (+0.146) |
| **Weighted κ** | — | **0.684** | **0.507** | 🟢 **Gemini wins** |

**Gemini outperforms OpenAI on every single dimension.**

---

## Key Findings

### Finding 1: Gemini is Substantially better than OpenAI
Gemini's weighted κ = 0.684 vs OpenAI's 0.507. This is a difference of 0.177 — nearly 3 classification levels apart. OpenAI produces only Moderate agreement with human raters overall.

### Finding 2: Correctness is the most reliable dimension
Gemini achieves Almost Perfect on Correctness (κ = 0.850), very close to human-human agreement (0.899). The improved rubrics — which correctly place edge cases under Completeness — are the main reason for this.

### Finding 3: Clarity and Efficiency are the hardest dimensions for LLMs
Both models struggle most on Clarity and Efficiency:
- Gemini: CLA=0.494, EFF=0.513 (Moderate)
- OpenAI: CLA=0.306, EFF=0.367 (Fair)

This reflects the inherent subjectivity of these dimensions. Clarity requires human judgment about readability. Efficiency requires understanding algorithmic intent — a task where GPT-4o-mini's lack of extended reasoning is most visible.

### Finding 4: OpenAI failed on Clarity — systematic bias
OpenAI's CLA = 0.306 (Fair) and exact agreement = only 32.5% means OpenAI and human raters **disagree more than 2 in 3 times** on Clarity. This is not random noise — it reflects a systematic bias where GPT-4o-mini conflates logical correctness with clarity, penalizing clear-but-wrong answers.

### Finding 5: The two LLMs fundamentally disagree with each other
Gemini vs OpenAI κ = 0.321 on Clarity and 0.418 on Completeness. When two evaluators disagree this much with each other, one of them must be consistently wrong relative to the human standard. The data clearly shows OpenAI is the divergent evaluator.

### Finding 6: Scale validation — 5 problems vs 10 problems
On 5 problems, Gemini achieved weighted κ = 0.740. On 10 problems, κ = 0.684. This is expected — more diverse problems reveal more edge cases where the LLM struggles. The 10-problem result is the more reliable estimate.

---

## Gap Analysis: Distance from Human Agreement

| Dimension | Human κ | Gemini κ | Gap | OpenAI κ | Gap |
|---|---|---|---|---|---|
| Correctness | 0.899 | 0.850 | **0.049** | 0.632 | 0.267 |
| Completeness | 0.878 | 0.646 | **0.232** | 0.521 | 0.357 |
| Clarity | 0.817 | 0.494 | **0.323** | 0.306 | 0.511 |
| Efficiency | 0.919 | 0.513 | **0.406** | 0.367 | 0.552 |

Gemini is significantly closer to human agreement on every dimension. The largest gap for Gemini is Efficiency (0.406) — this is the primary area for future improvement.

---

## Recommendation

**Use Gemini 2.5 Flash as the evaluation model.** It achieves:
- Almost Perfect on the most important dimension (Correctness, 40% weight)
- Substantial overall weighted κ = 0.684
- Consistent performance across both human raters (R1 vs Gemini ≈ R2 vs Gemini)

**OpenAI GPT-4o-mini is not suitable** for this evaluation task in its current configuration:
- Moderate overall weighted κ = 0.507
- Fair on Clarity and Efficiency
- Severe Clarity bias (only 32.5% exact agreement)

---

## Future Work

1. **Efficiency improvement:** Reintroduce the `[FIX: Dimension confusion — Efficiency]` rule to reduce the 0.406 Efficiency gap. This was removed in V4 and appears to have hurt Efficiency at scale (0.613 on 5 problems → 0.513 on 10 problems).
2. **Expand to all 15 problems** for a final production baseline.
3. **Investigate OpenAI with FIX rules:** The FIX rules (especially Clarity independence and Absence penalization) might significantly improve OpenAI's performance if tested.
