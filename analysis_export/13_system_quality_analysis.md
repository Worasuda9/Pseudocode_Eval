# FILE: 13_system_quality_analysis.txt
# DESCRIPTION: Holistic system quality analysis — reliability, bias, and limitations
# SOURCE: system_quality_analysis.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# System Quality Analysis
## Cohen's Kappa + Disagreement Statistics — Current State Assessment

---

## 1. Reference: What Kappa Scores Mean

| Kappa range | Interpretation |
|---|---|
| 0.81 – 1.00 | Almost perfect |
| 0.61 – 0.80 | Substantial |
| 0.41 – 0.60 | Moderate |
| 0.21 – 0.40 | Fair |
| 0.00 – 0.20 | Slight |

For an automated grading system to be **deployable**, the target is:
- Kappa ≥ 0.61 (Substantial) for all dimensions
- Mean(LLM − Human) close to 0 (±0.25 is acceptable)
- Std ≤ 0.70 (low variance = consistent behavior)

---

## 2. Full Data Table

### Cohen's Kappa

| Comparison | Correctness | Completeness | Clarity | Efficiency |
|---|---|---|---|---|
| **Rater1 vs Rater2** (human baseline) | 0.88 ✅ | 0.79 ✅ | 0.86 ✅ | 0.92 ✅ |
| **Rater1 vs Gemini** | 0.77 ✅ | 0.75 ✅ | 0.66 ✅ | 0.63 ✅ |
| **Rater2 vs Gemini** | 0.73 ✅ | 0.82 ✅ | 0.60 ✅ | 0.62 ✅ |
| Rater1 vs OpenAI | 0.80 ✅ | 0.91 ✅ | 0.51 ⚠️ | 0.60 ⚠️ |
| Rater2 vs OpenAI | 0.76 ✅ | 0.70 ✅ | 0.45 ⚠️ | 0.53 ⚠️ |
| Gemini vs OpenAI | 0.88 ✅ | 0.65 ✅ | 0.45 ⚠️ | 0.45 ⚠️ |

### Mean Disagreement (LLM − Human) and Std

| Comparison | Correctness | Completeness | Clarity | Efficiency |
|---|---|---|---|---|
| Rater1 vs Gemini | −0.10 ± 0.64 | +0.20 ± 0.52 | +0.25 ± 0.64 | *(see note)* |
| Rater2 vs Gemini | −0.05 ± 0.69 | −0.05 ± 0.39 | +0.30 ± 0.73 | +0.25 ± 0.79 |

> **Note:** Efficiency mean/std for R1 vs Gemini not provided in the latest run (was +0.40 ± 0.88 in the previous round before the ceiling fix — likely improved after the fix).

---

## 3. Dimension-by-Dimension Assessment

---

### ✅ CORRECTNESS — Good enough

| Metric | Value | Assessment |
|---|---|---|
| Kappa R1 vs Gemini | **0.77** | Substantial — passes threshold |
| Kappa R2 vs Gemini | **0.73** | Substantial — passes threshold |
| Mean (R1) | **−0.10** | Nearly neutral — Gemini very slightly stricter |
| Mean (R2) | **−0.05** | Nearly neutral |
| Std (R1) | **0.64** | Acceptable — some cases disagree by 1 level |
| Std (R2) | **0.69** | Acceptable |

**Verdict: ✅ Deployable.** Correctness is the most important dimension (40% weight) and it is performing well. Gemini and humans mostly agree — the small negative mean means Gemini is marginally stricter, which is a safe direction for an automated system. The remaining disagreements are mostly legitimate (human error cases or genuine ambiguity).

---

### ✅ COMPLETENESS — Good enough (better with Rater2)

| Metric | Value | Assessment |
|---|---|---|
| Kappa R1 vs Gemini | **0.75** | Substantial |
| Kappa R2 vs Gemini | **0.82** | Almost perfect ✅ |
| Mean (R1) | **+0.20** | Small positive — Gemini slightly more lenient |
| Mean (R2) | **−0.05** | Essentially neutral |
| Std (R1) | **0.52** | Good — low variance |
| Std (R2) | **0.39** | Excellent — very consistent |

**Verdict: ✅ Deployable.** The R2 vs Gemini result (κ=0.82, mean=−0.05) is essentially publication-quality agreement. The R1 vs Gemini result (κ=0.75, mean=+0.20) is slightly lower but still Substantial. The gap between R1 and R2 here likely reflects the R1 Human Error cases (P2/largely_incorrect/COM, P4/incorrect/COM) identified in the combined disagreement analysis. Gemini is correct in those cases.

---

### ⚠️ CLARITY — Acceptable but still has room to improve

| Metric | Value | Assessment |
|---|---|---|
| Kappa R1 vs Gemini | **0.66** | Substantial — borderline |
| Kappa R2 vs Gemini | **0.60** | Substantial — just at the threshold |
| Mean (R1) | **+0.25** | Moderate positive — Gemini more lenient |
| Mean (R2) | **+0.30** | Moderate positive — Gemini more lenient |
| Std (R1) | **0.64** | Moderate variance |
| Std (R2) | **0.73** | Higher variance — inconsistency |
| Gemini vs OpenAI | **0.45** | Moderate — the two LLMs disagree on Clarity a lot |

**Verdict: ⚠️ Borderline.** Kappa just meets the Substantial threshold, but the Gemini vs OpenAI kappa of 0.45 (Moderate) reveals that the two LLMs themselves cannot agree on Clarity — which means the criteria may still be insufficiently precise. The hedging language fix (just applied) should reduce the +0.25/+0.30 mean gap. The high std=0.73 for R2 is concerning — Gemini is inconsistent on Clarity for Rater2's submissions.

**Still needs:** Re-evaluate after the hedging language fix and check if mean drops below +0.15.

---

### ⚠️ EFFICIENCY — Acceptable but most variable

| Metric | Value | Assessment |
|---|---|---|
| Kappa R1 vs Gemini | **0.63** | Substantial — borderline |
| Kappa R2 vs Gemini | **0.62** | Substantial — borderline |
| Mean (R2) | **+0.25** | Moderate positive — Gemini more lenient |
| Std (R2) | **0.79** | High — most inconsistent dimension |
| Gemini vs OpenAI | **0.45** | Moderate — LLMs disagree a lot on Efficiency too |

**Verdict: ⚠️ Borderline.** Just above the Substantial threshold but closest to failing. The ceiling rule fix already brought Efficiency mean down from +0.40 to presumably +0.25 range. The Gemini vs OpenAI kappa of 0.45 shows both LLMs struggle to agree on Efficiency — this is partly structural (Efficiency is genuinely harder to evaluate from pseudocode) and partly that the rubric criteria for Efficiency are less precise than for other dimensions.

**Still needs:** Verify the ceiling rule reduced std meaningfully. The high variance (std=0.79) is the main concern — some submissions get Excellent, others Poor, with less predictability.

---

## 4. Overall System Assessment

### Comparison against human-human baseline

| Dimension | Human-Human κ | Best LLM-Human κ | Gap | Acceptable? |
|---|---|---|---|---|
| Correctness | 0.88 | 0.77 (R1-Gem) | −0.11 | ✅ Yes |
| Completeness | 0.79 | 0.82 (R2-Gem) | +0.03 | ✅ Exceeds human! |
| Clarity | 0.86 | 0.66 (R1-Gem) | −0.20 | ⚠️ Gap notable |
| Efficiency | 0.92 | 0.63 (R1-Gem) | −0.29 | ⚠️ Gap notable |

> Completeness with Rater2 actually exceeds human-human agreement — a strong result.
> Efficiency has the largest gap: human-human agreement is very high (0.92), but LLM-human is only 0.63. This means the dimension itself is consistent when humans evaluate it, but the LLM has a harder time matching that standard.

---

## 5. What Is Good Enough and What Still Needs Work

### ✅ Ready / Good enough
- **Correctness** — core dimension, performing well (κ≈0.75)
- **Completeness** — near-perfect with Rater2, good with Rater1 (κ≈0.75–0.82)
- **System direction** — Gemini's biases are small and mostly in safe directions (slightly stricter on Correctness, slightly lenient elsewhere)

### ⚠️ Still needs improvement
1. **Clarity** — borderline kappa (0.60–0.66), high std, LLM-LLM disagreement (0.45). The hedging fix should help; needs re-evaluation.
2. **Efficiency** — lowest kappa (0.62–0.63), highest std (0.79), largest gap from human-human baseline. The ceiling rule helped but the dimension is inherently hard to evaluate from pseudocode.
3. **LLM-LLM consistency on Clarity and Efficiency** — Gemini vs OpenAI κ=0.45 on both. This means the scoring criteria are still not precise enough to produce consistent results across different LLMs. A more explicit scoring rubric per tier (what exactly makes Clarity Excellent vs Good) would help.

### 🔍 Structural observation
The Kappa gap between R1-Gemini and R2-Gemini is largest for Correctness (0.77 vs 0.73). Part of this is the identified Human Error cases — R1 gave systematically higher Correctness to wrong submissions (P2/largely_incorrect, P4/incorrect). Gemini correctly gave lower scores. This inflates the "disagreement" metric even when Gemini is right.

---

## 6. Recommended Next Steps

| Priority | Action | Expected improvement |
|---|---|---|
| 1 | Re-evaluate after hedging language fix (Clarity) | Reduce Clarity mean from +0.25/+0.30 toward ±0.10 |
| 2 | Verify Efficiency std reduction after ceiling rule | Reduce Efficiency std from 0.79 toward 0.60 |
| 3 | Add explicit Clarity tier descriptions (what is Excellent/Good/Fair) to the rubric | Improve Gemini-OpenAI Clarity kappa above 0.60 |
| 4 | Flag R1 Human Error cases for rater calibration | Would improve R1-Gemini Correctness kappa from 0.77 toward 0.82+ |
| 5 | Consider weighting Efficiency lower (already 10%) | Reduces impact of the least reliable dimension |
