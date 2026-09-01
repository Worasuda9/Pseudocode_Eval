# FILE: 16_gemini_vs_openai_analysis.txt
# DESCRIPTION: Corrected Gemini vs OpenAI comparison — separate rater Kappa + score distributions
# SOURCE: gemini_vs_openai_analysis.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Gemini vs OpenAI Evaluation Behavior Analysis (Corrected)

> **Methodology Note:** All Kappa scores are reported per rater separately — not combined or averaged.  
> OpenAI evaluation was run on **40 submissions** (10 problems × 4 submissions), not 60.  
> Human baseline uses all 60 submissions (15 problems × 4 submissions).

---

## 1. Kappa Scores — Separate Rater Comparison

| Comparison | Correctness | Completeness | Clarity | Efficiency | **Average** |
|---|---|---|---|---|---|
| **Rater 1 vs Gemini** | **0.815** | **0.626** | **0.437** | **0.586** | **0.616** |
| **Rater 2 vs Gemini** | **0.854** | **0.698** | **0.401** | **0.604** | **0.639** |
| **Rater 1 vs OpenAI** | 0.628 | 0.580 | 0.311 | 0.366 | **0.471** |
| **Rater 2 vs OpenAI** | 0.636 | 0.461 | 0.301 | 0.368 | **0.441** |
| **Rater 1 vs Rater 2** *(ceiling)* | 0.882 | 0.837 | 0.823 | 0.882 | **0.856** |
| **Gemini vs OpenAI** | 0.658 | 0.418 | 0.321 | 0.494 | **0.473** |

> **Important:** OpenAI Kappa (n=40) is not directly comparable to Gemini Kappa (n=60) due to different dataset sizes. Gemini was run on 15 problems, OpenAI on 10 problems.

### Key Conclusion from Kappa Comparison
- **Gemini significantly outperforms OpenAI** on agreement with human raters on the current V4 prompt
  - Rater 1: Gemini avg **0.616** vs OpenAI **0.471** — Gemini wins by +0.145κ
  - Rater 2: Gemini avg **0.639** vs OpenAI **0.441** — Gemini wins by +0.198κ
- The earlier result showing identical Kappa for both models was a **data matching bug** in the comparison script (different keys were being used)
- Even Gemini vs OpenAI only reaches κ = 0.473 — meaning the two models disagree substantially with each other

---

## 2. Score Distribution — Both Human Raters Shown

### CORRECTNESS
| Score | Gemini | OpenAI | Human 1 | Human 2 |
|---|---|---|---|---|
| Excellent | **14** | 1 | 14 | 14 |
| Good | 1 | 8 | 4 | 4 |
| Fair | 13 | 9 | 15 | 14 |
| Poor | 32 | 22 | 27 | 28 |

### COMPLETENESS
| Score | Gemini | OpenAI | Human 1 | Human 2 |
|---|---|---|---|---|
| Excellent | 7 | 1 | 11 | **14** |
| Good | 5 | 3 | 5 | 2 |
| Fair | 22 | 13 | 15 | 12 |
| Poor | 26 | 23 | 29 | 32 |

### CLARITY
| Score | Gemini | OpenAI | Human 1 | Human 2 |
|---|---|---|---|---|
| Excellent | **17** | 0 | 15 | 14 |
| Good | 9 | 8 | 19 | 20 |
| Fair | 26 | 19 | 21 | 19 |
| Poor | 8 | **13** | 5 | 7 |

### EFFICIENCY
| Score | Gemini | OpenAI | Human 1 | Human 2 |
|---|---|---|---|---|
| Excellent | **19** | 6 | 13 | 16 |
| Good | 8 | 4 | 14 | 10 |
| Fair | 6 | 6 | 16 | 16 |
| Poor | 27 | **24** | 17 | 18 |

---

## 3. Key Behavioral Differences (Corrected)

### Gemini: Lenient at the top, over-strict at the bottom
- **Correctness Excellent:** Gemini=14 ✅ matches both Human 1 (14) and Human 2 (14) perfectly
- **Clarity Excellent:** Gemini=17 ≈ Human 1 (15) ≈ Human 2 (14) — slightly generous but close
- **Efficiency Excellent:** Gemini=19, Human 1=13, Human 2=16 — over-awards Excellent
- **Efficiency Poor:** Gemini=27, Human 1=17, Human 2=18 — also over-penalizes Poor
- Gemini tends to **polarize** toward the extremes (more Excellent and more Poor than humans)

### OpenAI: Systematically harsher across all dimensions
- **Correctness Excellent:** OpenAI=1 vs humans' 14 — massively under-scores
- **Clarity Excellent:** OpenAI=**0** vs Human 1 (15), Human 2 (14) — never gives Excellent on Clarity
- **Clarity Poor:** OpenAI=13 vs Human 1 (5), Human 2 (7) — over-penalizes significantly
- OpenAI consistently awards fewer Excellent scores and more Poor/Fair scores than both human raters

---

## 4. Why Gemini Performs Better on V4 Prompt

The V4 prompt was **calibrated through iterative testing with Gemini**. Every adjustment we made — the strict tier anchors, the lenient FIX rules, the Socratic hint guidelines — was evaluated by comparing Gemini's output to human raters. As a result:
- Gemini's Correctness Excellent distribution now matches humans almost perfectly
- Gemini's Clarity Excellent distribution is close to human level

OpenAI sees the same prompt but applies a different internal scoring baseline. Its Excellent threshold is far higher, causing systematic under-scoring that reduces Kappa significantly.

**To improve OpenAI performance**, a separate calibration cycle would need to:
1. Lower the bar for Clarity Excellent (OpenAI gives it 0 times vs humans' 14–15)
2. Reduce over-use of Clarity Poor (OpenAI=13 vs humans' 5–7)
3. Calibrate Efficiency to avoid the extreme polarization

---

## 5. Summary Table

| Model | Rater 1 κ avg | Rater 2 κ avg | Dataset Size | Verdict |
|---|---|---|---|---|
| **Gemini** | **0.616** | **0.639** | 60 submissions | ✅ Substantial |
| **OpenAI** | 0.471 | 0.441 | 40 submissions | ⚠️ Moderate |
| Human-Human | 0.856 | 0.856 | 60 submissions | ✅ Ceiling |
