# FILE: 15_gemini_behavior_analysis.txt
# DESCRIPTION: Deep analysis of Gemini scoring behavior across all 10 prompt versions
# SOURCE: gemini_behavior_analysis.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Gemini Evaluation Behavior — Deep Analysis Across All Prompt Versions

## 1. Kappa Score Evolution

| Version | Correctness | Completeness | Clarity | Efficiency | **Avg** |
|---|---|---|---|---|---|
| V1 (Baseline) | 0.709 | 0.720 | 0.521 | 0.425 | **0.594** |
| V3 | 0.648 | 0.734 | **0.631** | 0.625 | **0.660** |
| V3.5 (Mixed strict+lenient) | 0.648 | 0.734 | 0.502 | 0.498 | **0.595** |
| V3.6 | 0.713 | 0.734 | 0.447 | **0.662** | **0.639** |
| V4 (Old Rubrics) | 0.709 | 0.816 | 0.533 | 0.585 | **0.661** |
| **V4 (New Rubrics)** | 0.648 | 0.775 | **0.629** | **0.690** | **0.686** ← Best |
| V4.1 (+ EFF FIX) | 0.713 | 0.718 | 0.482 | 0.513 | **0.606** |
| V4.2 (Dim Sep blocks) | 0.751 | 0.677 | 0.537 | 0.613 | **0.645** |
| V4.3 (Mixed tiers) | 0.744 | 0.516 | 0.469 | 0.487 | **0.554** |
| **V4 FINAL (15 problems)** | **0.826** | 0.677 | 0.449 | 0.551 | **0.626** |

> **Human-human ceiling: κ = 0.856** — No LLM should be expected to exceed this.

---

## 2. Score Distribution Analysis

### Correctness
| Version | Excellent | Good | Fair | Poor |
|---|---|---|---|---|
| Human (5p) | 5 | 2 | 7 | 6 |
| V1 | 5 | **0** | 5 | 10 |
| V3 | 6 | **0** | 3 | 11 |
| V4 (old/new rubrics) | 5–6 | **0** | 3–5 | 10–11 |
| V4 FINAL (15p, normalized) | ~4.9 | ~0.4 | ~4.0 | ~10.7 |

**Key Pattern:** Gemini almost **never** gives "Good" for Correctness across every version — it jumps directly from Excellent to Fair. Humans give "Good" regularly (2 out of 20). This is a consistent Gemini behavior: it treats Correctness as a binary (either right or not) rather than a spectrum. This explains why Correctness Kappa plateaus around 0.71–0.83 despite all our improvements.

---

### Completeness
| Version | Excellent | Good | Fair | Poor |
|---|---|---|---|---|
| Human (5p) | 3 | 3 | 5 | 9 |
| V1 | 3 | 2 | 7 | 8 |
| V3 | **5** | 0 | 7 | 8 |
| V4 (old rubrics) | **5** | 0 | 7 | 8 |
| V4 (new rubrics) | **5** | 0 | 7 | 8 |
| V4.1 (EFF FIX) | 3 | 2 | **8** | 7 |

**Key Pattern:** Completeness scores are remarkably **stable across V1 to V4 new rubrics** — almost no change in distribution despite significant prompt rewrites. The biggest jump comes from the rubric quality, not the evaluation prompt. When rubrics were generic (V1–V3), Gemini gave more Excellent on Completeness incorrectly. The new rubrics gave it better anchors to identify what was truly missing, which is why Completeness Kappa jumped from 0.720 (V1) to 0.816 (V4 old rubrics) to 0.775 (V4 new rubrics).

---

### Clarity
| Version | Excellent | Good | Fair | Poor |
|---|---|---|---|---|
| Human (5p) | 5 | 4 | 8 | 3 |
| V1 | 6 | 1 | 8 | **5** |
| V3 | 5 | 6 | 9 | **0** |
| V3.5 | 6 | 7 | 7 | **0** |
| V4 (old rubrics) | 6 | 7 | 5 | 2 |
| V4 (new rubrics) | 7 | 5 | 6 | 2 |

**Key Pattern:** Clarity reveals the most dramatic behavioral shift across versions.
- **V1:** Too many "Poor" scores (5 vs human's 3) — too harsh
- **V3/V3.5:** Completely **eliminated "Poor"** (0 times) — too lenient, never penalized genuinely unclear submissions
- **V4:** Restored "Poor" (2 times) but still slightly under-penalizes relative to humans (3)

This is why V3 had the highest Clarity Kappa (0.631) — the lenient distribution accidentally matched humans better. V4's stricter tiers re-introduced some harshness that doesn't quite match human rater judgment on subjective readability.

**Root cause:** Clarity is inherently subjective. Gemini's model of "is this clear?" does not consistently match how human teachers perceive clarity in student writing.

---

### Efficiency
| Version | Excellent | Good | Fair | Poor |
|---|---|---|---|---|
| Human (5p) | 5 | 4 | 6 | 5 |
| V1 | 6 | 0 | 4 | **10** |
| V3 | 6 | 6 | 6 | 2 |
| V4 (old rubrics) | 4 | **7** | 5 | 4 |
| V4 (new rubrics) | **8** | 2 | 6 | 4 |

**Key Pattern:** Efficiency shows the biggest volatility across versions — meaning the prompt instructions most strongly control this dimension.
- **V1:** Massively over-penalized with Poor (10 vs human's 5) — model was refusing to score Efficiency when Correctness was low
- **V3:** Balanced distribution, closest to humans — explains V3's high Efficiency Kappa (0.625)
- **V4 new rubrics:** Over-awarded Excellent (8 vs human's 5) — after the EFF FIX rule was added, the model became too generous

This confirms: **Efficiency is the most prompt-sensitive dimension.** A small change in wording causes big swings in how the model scores it.

---

## 3. Behavioral Fingerprints — Summary

| Gemini Behavior | Consistent Across All Versions? | Impact |
|---|---|---|
| Almost never gives "Good" for Correctness | ✅ Yes — every version | Correctness Kappa plateaus at ~0.83 |
| Eliminates "Poor" for Clarity when prompt is lenient | ✅ Yes (V3, V3.5) | Short-term Kappa boost, long-term instability |
| Highly sensitive to Efficiency wording | ✅ Yes | Biggest Kappa swings on Efficiency |
| Completeness stable across prompt changes | ✅ Yes | Rubric quality matters more than prompt for Completeness |
| Never gives "Good" for Completeness (pre-V4.1) | ✅ Yes (V1–V4) | Completeness is also treated as near-binary |

---

## 4. Key Takeaway for Presentation

> **Gemini treats evaluation as a classification task with strong anchor bias.** It naturally gravitates toward the two extremes (Excellent or Poor/Fair) and rarely uses the middle tier (Good). This is fundamentally different from human raters who use the full spectrum consistently.
>
> The most effective prompt engineering intervention was **not changing the evaluation logic** — it was **improving the rubrics**. Better rubrics gave Gemini clearer anchors, which reduced its tendency to jump between extremes and improved alignment with human judgment by ~0.09κ average.
