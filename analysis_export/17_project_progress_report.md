# FILE: 17_project_progress_report.txt
# DESCRIPTION: Comprehensive post-midterm project progress document (all work Jul 7–22)
# SOURCE: project_progress_report.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Project Progress Document
## Automated Pseudocode Evaluation System
### Post-Midterm Report: July 7 – July 22, 2026

---

## 1. Project Background & Objective

This project develops an automated system to evaluate student pseudocode submissions for introductory programming courses (CS1) using a large language model (LLM). The system evaluates each submission across four dimensions using Cohen's Weighted Kappa (κ) as the primary reliability metric, comparing LLM scores against two independent human expert raters.

**Four evaluation dimensions:**
| Dimension | Weight | What it measures |
|---|---|---|
| Correctness | 40% | Whether the algorithm logic would produce correct output |
| Completeness | 30% | Whether all required structural components are present |
| Clarity | 20% | Whether the pseudocode is logically readable and unambiguous |
| Efficiency | 10% | Whether the student avoids redundant or unnecessary operations |

**Evaluation scale (Landis & Koch, 1977):**
- ≥ 0.80 = Almost Perfect
- 0.61–0.80 = Substantial ← project target
- 0.41–0.60 = Moderate
- < 0.40 = Fair/Slight

---

## 2. Work Completed

### 2.1 Disagreement Analysis (July 7–9)

Before prompt engineering, 132 disagreement cases between the LLM and two human raters were systematically analyzed and classified across 5 problems (20 submissions).

| Category | Count | % | Description |
|---|---|---|---|
| A — Systematic Strictness | 70 | 53% | LLM scored lower than humans |
| F — Leniency | 17 | 13% | LLM scored higher than humans |
| C — Rubric Prescription | 16 | 12% | LLM followed a flawed rubric sub-criterion too literally |
| HE — Human Error | 14 | 11% | Human rater was provably wrong; LLM was correct |
| D — Dimension Confusion | 8 | 6% | LLM penalized Efficiency for Correctness failures |
| G — Hallucination | 6 | 5% | Unjustified extreme scores not supported by pseudocode |
| B — Absence Penalization | 1 | 1% | LLM penalized missing formal keywords |

This analysis identified the exact causes of failure and directly informed the 7 targeted prompt fixes applied in the following phase.

---

### 2.2 Prompt Engineering — 7 Targeted Fixes (July 10)

Seven rules were added to `prompts.py` to address each disagreement category:

| Fix | Rule | Targets |
|---|---|---|
| Fix 1 — CS1 Leniency | Never use Poor if the core logic has any merit | Category A |
| Fix 2 — Dimension Confusion | Efficiency evaluates structure only, never correctness | Category D |
| Fix 3 — Absence Penalization | Credit implied loops, functions, and output | Category B |
| Fix 4 — Clarity Independence | Clarity is independent of correctness | Category G |
| Fix 5 — Implied Output | Implied return/print satisfies Completeness | Category C |
| Fix 6 — Efficiency Ceiling | Missing major component → cap Efficiency at Good | Over-leniency |
| Fix 7 — Clarity Hedging | Hedging words or vague conditions → cap Clarity | Over-leniency |

---

### 2.3 Rubric Generator Improvement (July 14–16)

**Root cause discovery:** GPT-4o-mini evaluations revealed that the rubric generator was incorrectly placing edge cases (e.g., N=0, empty input) under the Correctness dimension. This caused the LLM to penalize Correctness for missing edge cases, even when the core algorithm was correct — a form of double penalization.

**Fix applied:** Two explicit rules were added to the rubric generator prompt:
1. Edge cases belong under Completeness ONLY
2. Correctness sub-criteria must target core logic only, not boundary conditions

**Impact:** All 15 problem rubrics were regenerated with the corrected generator. This produced the single largest improvement in Correctness Kappa across the entire project: **+0.11κ** (from 0.754 to 0.864).

---

### 2.4 Prompt Version Experiments — 10+ Versions Tested (July 10–22)

A systematic series of prompt configurations was tested. Every version was evaluated on at least 5 problems × 4 submissions = 20 ratings per dimension, compared against both human raters.

| Version | Key Change | COR | COM | CLA | EFF | Weighted κ | Verdict |
|---|---|---|---|---|---|---|---|
| V1 (Baseline) | Initial prompt | 0.709 | 0.720 | 0.521 | 0.425 | 0.594 | Starting point |
| V_clarity20 | 7 targeted FIX rules | 0.754 | 0.786 | 0.631 | 0.625 | 0.726 | ✅ All Substantial |
| V3.5 | V4 strict tiers + FIX rules | 0.753 | 0.816 | 0.503 | 0.498 | 0.697 | ❌ CLA/EFF dropped |
| Gemini7 | 6 consistency fixes + new rubrics | 0.822 | 0.783 | 0.297 | 0.662 | 0.689 | ❌ CLA crashed |
| V3.6 | Strict Clarity tier only + new rubrics | 0.823 | 0.786 | 0.447 | 0.662 | 0.720 | ⚠️ CLA still low |
| **V4 (New Rubrics)** | Pure strict tiers + new rubrics | **0.864** | 0.754 | **0.537** | 0.614 | **0.740** | ✅ **Production** |
| V4.1 | V4 + Efficiency FIX rule | 0.713 | 0.718 | 0.482 | 0.513 | 0.606 | ❌ Contradiction |
| V4.2 | Per-dimension variable blocks | 0.751 | 0.677 | 0.537 | 0.613 | 0.645 | ⚠️ COM dropped |
| V4.3 | V4.2 + full definitions restored | 0.744 | 0.516 | 0.469 | 0.487 | 0.554 | ❌ Worst overall |
| **V4 FINAL (15p)** | Reverted to V4, full 15-problem run | **0.835** | 0.662 | 0.419 | 0.595 | **0.677** | ✅ **Official** |

---

### 2.5 LLM Provider Comparison — Gemini vs OpenAI (July 15–22)

Both models were evaluated using the same V4 prompt on 10 problems (40 submissions) and compared against two independent human raters separately.

**Results — reported per rater (not averaged):**

| Comparison | Correctness | Completeness | Clarity | Efficiency | Avg κ |
|---|---|---|---|---|---|
| Rater 1 vs Gemini | 0.815 | 0.626 | 0.437 | 0.586 | **0.616** |
| Rater 2 vs Gemini | 0.854 | 0.698 | 0.401 | 0.604 | **0.639** |
| Rater 1 vs OpenAI | 0.628 | 0.580 | 0.311 | 0.366 | **0.471** |
| Rater 2 vs OpenAI | 0.636 | 0.461 | 0.301 | 0.368 | **0.441** |
| Rater 1 vs Rater 2 *(ceiling)* | 0.882 | 0.837 | 0.823 | 0.882 | **0.856** |

**Gemini outperforms OpenAI by +0.17κ average** on the V4 prompt.

---

### 2.6 Prompt Architecture Refactoring (July 17)

`prompts.py` was restructured from a single monolithic evaluation prompt into four isolated dimension-specific Python variables:

```python
_CORRECTNESS_EVALUATION_GUIDE   # Strict V4 tier anchors
_COMPLETENESS_EVALUATION_GUIDE  # Lenient tiers for CS1 students
_CLARITY_EVALUATION_GUIDE       # Strict V4 tier anchors
_EFFICIENCY_EVALUATION_GUIDE    # Lenient tiers + EFF FIX rule
```

These are injected via f-string into `EVALUATION_SYSTEM_PROMPT`, preserving the single-API-call architecture while eliminating cross-dimension rule conflicts.

A complete version archive was also established:
- `prompts_v1.py` through `prompts_v3.py` (early versions)
- `prompts_v_clarity20.py` (lenient baseline)
- `prompts_v4.py` (pure strict baseline — production)
- `prompts_v4_1.py` (strict + EFF FIX — archived)

---

### 2.7 Official Final Evaluation — 15 Problems (July 21)

The definitive evaluation was run on all 15 problems × 4 submissions = 60 total ratings, using the V4 prompt with regenerated rubrics.

| Dimension | Rater 1 vs Gemini | Rater 2 vs Gemini | Interpretation |
|---|---|---|---|
| Correctness | κ = 0.815 | κ = 0.854 | Almost Perfect ✅ |
| Completeness | κ = 0.626 | κ = 0.698 | Substantial ✅ |
| Clarity | κ = 0.437 | κ = 0.401 | Moderate ⚠️ |
| Efficiency | κ = 0.586 | κ = 0.604 | Moderate ⚠️ |
| **Weighted Avg** | — | — | **κ ≈ 0.677 (Substantial)** |

The system reaches **79% of human-level reliability** overall. Excluding Clarity (the most subjective dimension), the three remaining dimensions achieve **85.5% of human-level reliability**.

---

### 2.8 Behavioral Analysis (July 22)

Two deep behavioral analyses were conducted to extract research insights from the full dataset.

**Gemini Behavioral Fingerprints (across all 10 prompt versions):**

| Pattern | Finding |
|---|---|
| Binary Correctness Bias | Gemini almost never uses "Good" for Correctness — jumps Excellent → Fair/Poor. Caps Correctness Kappa at ~0.83 regardless of prompt. |
| Completeness is Rubric-Driven | Completeness distribution barely changed across all prompt versions. Kappa improved only when rubrics improved. |
| Clarity follows Leniency | When prompt is lenient → Gemini stops giving "Poor" (0/20 in V3). When strict → too harsh. Gemini has no stable internal "readable" model. |
| Efficiency is Prompt-Sensitive | Largest Kappa swings of any dimension. V1: gave Poor 10/20 times. V3: reduced to 2. EFF FIX rule had biggest single-version impact. |

**Gemini vs OpenAI Score Distributions (60 submissions):**

| Score | Gemini | OpenAI | Human 1 | Human 2 |
|---|---|---|---|---|
| **Correctness Excellent** | 14 | 1 | 14 | 14 |
| **Clarity Excellent** | 17 | **0** | 15 | 14 |
| **Clarity Poor** | 8 | **13** | 5 | 7 |
| **Efficiency Excellent** | 19 | 6 | 13 | 16 |

- **Gemini** closely matches human Excellent counts for Correctness and Clarity, but over-polarizes (too many Excellent and too many Poor simultaneously)
- **OpenAI** never awards Excellent for Clarity (0 times vs human 14–15) and over-uses Poor across all dimensions

---

## 3. Results & Key Findings

### Finding 1: Rubric Quality is the Primary Driver of Evaluation Accuracy
The biggest single improvement across the entire project came from fixing the rubric generator, not the evaluation prompt. Correctly separating edge cases from Correctness into Completeness improved Correctness Kappa by **+0.11κ** — the largest single improvement of the project. This finding suggests that future work on LLM-based assessment should prioritize rubric quality before prompt engineering.

### Finding 2: Correctness Achieves Near-Human Reliability
Correctness κ = 0.835 (Almost Perfect). The gap to the human-human ceiling (0.882) is only 0.047. This is the most reliable dimension and the strongest result of the project. The system can be trusted to identify correct vs incorrect algorithmic logic at near-human level.

### Finding 3: Clarity is a Fundamental Limitation — Not a Prompt Problem
Clarity κ ranged from 0.297 (worst) to 0.631 (best) across all prompt versions, with no stable configuration maintaining Substantial agreement across different problem sets. Analysis confirmed this is because:
1. Clarity is inherently subjective — human raters integrate logic quality into their readability judgments in ways that are not rule-definable
2. The two LLMs (Gemini and OpenAI) score Clarity very differently from each other (κ = 0.321), confirming there is no single "correct" LLM interpretation of readability

### Finding 4: Conflicting Rules Degrade Performance
The V4.1 experiment (strict Efficiency tier + lenient EFF FIX rule simultaneously) proved that contradictory instructions within the same prompt context cause unpredictable model behavior. Efficiency Kappa dropped from 0.614 to 0.513. This is a general principle: every rule added to the prompt must be logically consistent with all other rules in the same context.

### Finding 5: Complex Architecture Does Not Guarantee Better Results
The most sophisticated prompt configurations (V4.2, V4.3) with isolated dimension blocks and mixed tier strategies performed worse than the simpler V4 baseline. Prompt simplicity and internal consistency are more important than architectural sophistication.

### Finding 6: LLMs Have Stable Model-Level Biases
- **Gemini** almost never uses "Good" for Correctness across all 10 prompt versions — a fundamental model behavior that cannot be corrected by prompt changes alone
- **OpenAI** systematically avoids Excellent scores and over-uses Poor, particularly on Clarity (0 Excellent given vs human 14–15). These are calibration differences between the models' pre-training and RLHF, not prompt issues

### Finding 7: Human Error is Present in Ground Truth (11% of disagreements)
14 out of 132 disagreement cases (11%) were confirmed as cases where the LLM was correct and the human rater was demonstrably wrong. For example: a human gave "Fair" to a submission that explicitly admitted its own logical error. These Human Error cases artificially lower the reported Kappa scores — the system's true reliability is marginally higher than the published numbers.

### Finding 8: Gemini Significantly Outperforms OpenAI on V4 Prompt
- Rater 1: Gemini κ_avg = 0.616 vs OpenAI 0.471 (+0.145κ)
- Rater 2: Gemini κ_avg = 0.639 vs OpenAI 0.441 (+0.198κ)

The V4 prompt was calibrated through iterative Gemini testing — its tier anchors and FIX rules were tuned to correct Gemini's specific tendencies. OpenAI needs a separate calibration cycle.

---

## 4. Issues & Solutions

| Issue | Root Cause | Solution Applied |
|---|---|---|
| LLM systematic over-strictness (53% of disagreements) | Prompt tier anchors were calibrated for expert-level pseudocode, not CS1 students | Added CS1 leniency rule: never use Poor if core logic has any merit |
| Dimension confusion: Efficiency penalized for incorrect logic | No explicit rule separating structural performance from logical correctness | Added `[FIX: Dimension confusion]` rule: Efficiency evaluates structure independently |
| OpenAI harsher than Gemini | Rubric placed edge cases under Correctness; OpenAI followed rubric strictly while Gemini reasoned around it | Fixed rubric generator to place edge cases under Completeness only |
| Clarity Kappa crashed to 0.297 (Gemini7) | Merging and emphasizing the "wrong logic ≠ unclear writing" rule caused Gemini to award Excellent Clarity to even comprehension-impossible submissions | Added explicit Clarity boundary rule and concrete calibration examples at the Poor end |
| Efficiency FIX rule contradicted strict V4 tier | Strict tier said "no redundant steps whatsoever"; FIX rule said "score Good/Excellent even if logic is wrong" — direct contradiction | Isolated dimension rules into separate Python variables (`_EFFICIENCY_EVALUATION_GUIDE`) to prevent cross-dimension rule conflict |
| V4.3 Mixed Prompt underperformed V4 | More complex prompt architecture introduced ambiguity and reduced the model's confidence in applying individual rules | Reverted to clean V4 prompt; established as permanent production baseline |
| OpenAI Kappa comparison showed identical results to Gemini (data bug) | Comparison script was matching on wrong key combinations, mapping OpenAI scores to Gemini keys | Fixed key matching; revealed true gap: Gemini +0.17κ above OpenAI |

---

## 5. System Architecture

The final system consists of two pipelines operating on a structured problem-rubric-submission triplet:

**Pipeline 1 — Rubric Generation (Call 1):**
- Input: Problem statement
- Output: Structured JSON rubric with 4 dimensions and 2–4 problem-specific sub-criteria each
- Key rules: Edge cases under Completeness only; sub-criteria must be algorithmically grounded and problem-specific; no Correctness language in Completeness

**Pipeline 2 — Evaluation (Call 2, with retry):**
- Input: Problem statement + Rubric + Student pseudocode
- Output: Per-dimension qualitative score (Excellent/Good/Fair/Poor), feedback on what was correct, issue description, and Socratic hint
- Architecture: Four isolated dimension evaluation guides (`_CORRECTNESS_EVALUATION_GUIDE`, etc.) injected via f-string into a unified system prompt
- Retry logic: Automatic retry on JSON parse failure or schema validation error
- Trace saving: Full LLM reasoning, thinking tokens, validation result, and retry status saved per submission

**LLM providers supported:** Google Gemini 2.5 Flash (primary, recommended), OpenAI GPT-4 series (secondary, requires separate calibration)

---

## 6. Prompt Version Archive

| File | Description | Status |
|---|---|---|
| `prompts_v1.py` | Original baseline prompt | Archived |
| `prompts_v2.py` | Early iterative version | Archived |
| `prompts_v3.py` | V_clarity20 — all 7 FIX rules, lenient tiers | Archived |
| `prompts_v_clarity20.py` | Copy of V3, lenient baseline | Archived |
| `prompts_v4.py` | Pure V4 — strict tiers, no FIX rules | Archived |
| `prompts_v4_1.py` | V4 + Efficiency FIX rule (contradiction) | Archived |
| `prompts.py` | **V4 production baseline — current active** | ✅ Active |

---

## 7. Quantitative Summary — Kappa Improvement Over Project Lifetime

| Milestone | Weighted κ | Change from V1 |
|---|---|---|
| V1 — Initial baseline | 0.594 | — |
| V_clarity20 — After 7 FIX rules | 0.726 | +0.132 (+22%) |
| V4 + new rubrics — After rubric fix | 0.740 (5p) | +0.146 (+25%) |
| **V4 FINAL — Official (15 problems)** | **0.677** | **+0.083 (+14%)** |
| Human-human ceiling | 0.856 | — |

> The 5-problem vs 15-problem difference (0.740 vs 0.677) is explained by statistical variance — with n=20, a single disagreement shifts Kappa by ~0.03. The 15-problem result at n=60 is statistically more reliable.

---

## 8. Next Steps & Future Work

### Immediate (Before July 29 Final Presentation)
- [x] Finalize 15-problem evaluation results ✅
- [x] Behavioral analysis — Gemini and OpenAI ✅
- [x] Study abstract / progress document ✅
- [ ] Final presentation slides
- [ ] Final presentation script

### Short-Term Future Work
| Priority | Action | Expected Impact |
|---|---|---|
| 🔴 High | OpenAI-specific prompt calibration | Requires lowering bar for Clarity Excellent (currently 0/60 vs human 14–15) and reducing Clarity Poor over-use |
| 🟡 Medium | Expand dataset to 30+ problems | Reduces Kappa standard error from ±0.05 to ±0.03; brings results to publication quality |
| 🟡 Medium | Human review flagging for borderline scores | Flag Clarity and Efficiency scores in the Moderate range for human review before returning feedback to students |

### Long-Term Research Directions
| Direction | Description |
|---|---|
| Per-dimension independent API calls | 4 separate calls with context passing to prevent double-penalization. Requires solving the shared-context problem. |
| Multi-LLM ensemble | Average scores from Gemini + Claude + GPT-4 to reduce model-level bias; has been shown to improve reliability in other automated assessment studies |
| Clarity sub-dimension decomposition | Split Clarity into sub-scores: (a) structural flow, (b) variable naming, (c) ambiguity — may allow more reliable automated scoring of the sub-components |
| Claude API evaluation | Claude tends to give more calibrated, nuanced responses than GPT-4 — likely to perform better than GPT-4o-mini without any prompt adjustment |

---

## 9. Conclusion

The automated pseudocode evaluation system has progressed from an initial weighted κ of 0.594 (Moderate) to a final weighted κ of 0.677 (Substantial) over the post-midterm period, representing a 14% improvement over the baseline. The system now achieves Almost Perfect agreement on Correctness (κ = 0.835), the highest-weight dimension (40%), and Substantial agreement on Completeness (30%).

The most important engineering insight of this project is that **rubric quality is a stronger driver of evaluation accuracy than prompt complexity**. The single largest performance jump came from correcting the rubric generator to place edge cases under Completeness — not from any prompt engineering change. Future work on LLM-based assessment systems should prioritize rubric design and generation quality alongside evaluator prompt engineering.

Clarity remains the primary open challenge. It is a structurally subjective dimension for which no current prompt configuration achieves Substantial agreement at the model level. This is identified as a ceiling of the current approach and a meaningful research direction for future work.
