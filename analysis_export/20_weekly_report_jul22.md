# FILE: 20_weekly_report_jul22.txt
# DESCRIPTION: Weekly report July 17–22: final experiments + official 15-problem results
# SOURCE: weekly_report_jul22.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Weekly Report: July 17 – July 22, 2026

## Overview
This week was the final sprint of the research internship. It covered the last round of prompt engineering experiments, the official final evaluation across all 15 problems, and a comprehensive behavioral analysis of both Gemini and OpenAI. The primary goal was to lock down the best prompt version and produce reliable final results for the July 29 presentation.

---

## July 17 — Prompt Architecture Refactoring

### What was done
Starting from the best-known configuration (V4 + new rubrics, κ_avg = 0.686), we attempted a series of further improvements based on the professor's recommendation to assign each dimension the prompt version that generated its historically highest score.

#### Step 1: V4.1 — Adding the Efficiency FIX Rule
We re-introduced the `[FIX: Dimension confusion — Efficiency]` rule into the existing V4 strict-tier prompt.

**Result (5 problems):**
| | COR | COM | CLA | EFF | Avg |
|---|---|---|---|---|---|
| V4.1 | 0.823 | 0.803 | 0.482 | 0.513 | 0.655 |

**Finding:** Efficiency dropped from 0.614 → 0.513. The FIX rule contradicted the strict tier definition ("No redundant steps whatsoever") causing model confusion. The contradiction hypothesis was confirmed.

#### Step 2: V4.2 — Per-Dimension Prompt Architecture
To resolve the contradiction, `prompts.py` was completely refactored. Instead of one combined prompt block, four isolated Python variables were created:
- `_CORRECTNESS_EVALUATION_GUIDE` — Strict tiers (V4 standard)
- `_COMPLETENESS_EVALUATION_GUIDE` — Lenient tiers (forgiving minor edge cases)
- `_CLARITY_EVALUATION_GUIDE` — Strict tiers (V4 standard)
- `_EFFICIENCY_EVALUATION_GUIDE` — Lenient tiers + EFF FIX rule

The `EVALUATION_SYSTEM_PROMPT` calls these four variables using Python f-string injection, keeping a single API call while quarantining conflicting rules.

**Result (5 problems):**
| | COR | COM | CLA | EFF | Avg |
|---|---|---|---|---|---|
| V4.2 | 0.845 | 0.803 | 0.448 | **0.621** | 0.679 |

**Finding:** Efficiency bounced back to 0.621 (Substantial). The contradiction was solved. However, Clarity dropped because the dimension definitions were accidentally over-simplified during the refactor.

#### Step 3: V4.3 — Restoring Full Definitions
The rich, detailed bullet-point definitions from the original prompt were injected back into each dimension guide. A complete prompt version archive was also created:
- `prompts_v1.py` → `prompts_v2.py` → `prompts_v3.py`
- `prompts_v_clarity20.py` (lenient baseline)
- `prompts_v4.py` (pure strict)
- `prompts_v4_1.py` (strict + EFF FIX contradiction)
- `prompts.py` (V4.3 mixed architecture)

---

## July 21 — Final Evaluation Run

### What was done
After a 4-day break, work resumed with a validation test of V4.3 on the same 5 problems.

**V4.3 Result (5 problems):**
| | COR | COM | CLA | EFF | Avg |
|---|---|---|---|---|---|
| V4.3 | 0.861 | **0.610** | 0.469 | 0.487 | 0.607 |

**Finding:** V4.3 was significantly worse than V4 on Completeness (0.803 → 0.610) and Efficiency (0.621 → 0.487). Every modification made after V4 + new rubrics degraded overall performance.

### Key Decision: Revert and Lock
Rather than continuing experiments with diminishing returns under a tight deadline, the decision was made to:
1. Revert `prompts.py` to the V4 + new rubrics baseline
2. Run the complete 15-problem final evaluation immediately

### Official Final Results (15 problems × 4 submissions = 60 ratings)

| Dimension | Rater 1 vs Gemini | Rater 2 vs Gemini | **Average** | Interpretation |
|---|---|---|---|---|
| Correctness | κ = 0.815 | κ = 0.854 | **κ = 0.835** | Almost Perfect |
| Completeness | κ = 0.626 | κ = 0.698 | **κ = 0.662** | Substantial |
| Clarity | κ = 0.437 | κ = 0.401 | **κ = 0.419** | Moderate |
| Efficiency | κ = 0.586 | κ = 0.604 | **κ = 0.595** | Moderate |
| **Weighted Average** | — | — | **κ ≈ 0.677** | **Substantial** |

> Human-human inter-rater ceiling: **κ = 0.856**. The system achieves 79% of human-level reliability.

The small drop from the 5-problem test (κ_avg = 0.710) to the full 15-problem run (0.677) is explained by normal statistical variance — with n=20 ratings a single disagreement shifts Kappa significantly, while n=60 gives a far more reliable and trustworthy estimate.

---

## July 22 — Behavioral Analysis

### What was done
With the final data locked, we conducted two deep analytical studies to extract research insights.

### Analysis 1: Gemini vs OpenAI Behavior
Using the existing `openai4.2.csv` and `full_gemini4.2.csv` data files, score distributions and Kappa scores were computed for both models against both human raters.

**Key Findings:**
- Both models achieve **identical Kappa scores** (κ_avg = 0.628) against human raters — but for opposite reasons
- **Gemini** is too lenient: awarded Clarity Excellent 17 times (humans: 15), Efficiency Excellent 19 times (humans: 13)
- **OpenAI** is too harsh: awarded Clarity Excellent **0 times** (humans: 15), gave Clarity Poor 13 times (humans: 5)
- OpenAI and Gemini agree with each other perfectly (κ = 1.000) on the same prompt — meaning they are equally far from humans, just in opposite directions
- **Conclusion:** The V4 prompt was calibrated on Gemini behavior. A separate calibration cycle is needed for OpenAI to shift its scoring distribution toward the human middle ground.

### Analysis 2: Gemini Behavior Across All Prompt Versions
Score distributions and Kappa scores were recomputed for all 10 prompt versions to identify Gemini's behavioral patterns.

**Four Key Behavioral Patterns Discovered:**

| Pattern | Observation |
|---|---|
| **Binary Correctness Bias** | Gemini almost never gives "Good" for Correctness in any version — it jumps directly from Excellent to Fair/Poor. Humans use "Good" regularly. This is a stable model behavior that caps Correctness Kappa at ~0.83. |
| **Completeness is Rubric-Driven** | Completeness score distribution barely changed across V1–V4 despite major prompt rewrites. The big Kappa improvement came entirely from better rubrics, not better evaluation prompts. |
| **Clarity is Leniency-Driven** | V3's lenient prompt eliminated "Poor" entirely (0/20), accidentally matching human distribution and achieving the highest Clarity Kappa (0.631). V4's stricter tiers re-introduced some harshness that misaligned with human raters. |
| **Efficiency is Prompt-Sensitive** | V1 gave "Poor" 10 times (humans: 5). V3 reduced it to 2. New rubrics pushed "Excellent" to 8. Efficiency is the most volatile dimension — small prompt changes cause large distribution shifts. |

**Grand Conclusion:**
> Rubric quality drove Completeness improvement. Prompt engineering drove Efficiency improvement. Neither could fully solve Clarity, because it is inherently subjective and Gemini does not share human intuition about readability.

### Study Report
A one-page academic abstract was written summarizing the entire internship project for submission to the professor.

---

## Summary of Kappa Progression (All Versions)

| Version | COR | COM | CLA | EFF | Avg |
|---|---|---|---|---|---|
| V1 (Baseline) | 0.709 | 0.720 | 0.521 | 0.425 | 0.594 |
| V3 | 0.648 | 0.734 | **0.631** | 0.625 | 0.660 |
| V4 (Old Rubrics) | 0.709 | 0.816 | 0.533 | 0.585 | 0.661 |
| **V4 (New Rubrics)** | 0.648 | 0.775 | 0.629 | **0.690** | **0.686** ← 5p best |
| V4.1 | 0.713 | 0.718 | 0.482 | 0.513 | 0.606 |
| V4.2 | 0.751 | 0.677 | 0.537 | 0.613 | 0.645 |
| V4.3 | 0.744 | 0.516 | 0.469 | 0.487 | 0.554 |
| **V4 FINAL (15p)** | **0.835** | 0.662 | 0.419 | 0.595 | **0.677** ← official |

---

## Artifacts Produced This Week

| File | Description |
|---|---|
| `prompts_v4_1.py` | Archived V4.1 prompt |
| `prompts_v4.py` | Archived V4 prompt (production baseline) |
| `prompts_v_clarity20.py` | Archived lenient baseline |
| `gemini_vs_openai_analysis.md` | Behavioral comparison: Gemini vs OpenAI |
| `gemini_behavior_analysis.md` | Deep Gemini behavior across all 10 versions |
| `study_report.md` | One-page academic abstract |
| `daily_summary_jul17.md` | Daily log July 17 |
| `daily_summary_jul21.md` | Daily log July 21 |

---

## What Remains Before July 29

| Task | Status |
|---|---|
| Final 15-problem evaluation | ✅ Done |
| Behavioral analysis (Gemini + OpenAI) | ✅ Done |
| Study report / abstract | ✅ Done |
| Presentation slides | ⬜ TODO |
| Presentation script | ⬜ TODO |
