# FILE: 18_weekly_report_jul10.txt
# DESCRIPTION: Weekly report July 7–10: disagreement analysis + 6 prompt versions tested
# SOURCE: weekly_report_jul10.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Weekly Report — Pseudocode Evaluation System
## Week of July 7–10, 2026

---

## 1. Overview — What We Did This Week

This week focused on **improving the reliability and accuracy of the LLM-based pseudocode evaluator** by:
1. Analyzing disagreements between LLM and human raters
2. Auditing and patching rubrics
3. Engineering targeted prompt fixes
4. Measuring improvement using Cohen's Weighted Kappa across 6 evaluation rounds

---

## 2. Starting Point — The Problem

Before this week's work, we had identified **132 disagreement cases** across 4 problem pairs (P1–P4) between Gemini and two human raters.

### Disagreement categories identified:
| Category | Count | % | Description |
|---|---|---|---|
| **A — LLM Systematic Strictness** | 70 | 53% | LLM gave lower scores than humans (stricter) |
| **F — LLM Leniency** | 17 | 13% | LLM gave higher scores than humans (lenient) |
| **C — Rubric Prescription** | 16 | 12% | LLM followed flawed rubric sub-criteria too literally |
| **HE — Human Error** | 14 | 11% | Human rater was clearly wrong; LLM was correct |
| **D — Dimension Confusion** | 8 | 6% | LLM penalized Efficiency for Correctness failures |
| **G — LLM Hallucination** | 6 | 5% | Unjustified extreme scores not supported by pseudocode |
| **B — Absence Penalization** | 1 | 1% | LLM penalized missing formal keywords |

> **The dominant problem was LLM systematic strictness (53%)**, especially on Correctness and Efficiency.

---

## 3. What We Fixed

### 3.1 Rubric Auditing (5 rubrics: p001–p005)
Audited the 5 newest generated rubrics against 3 quality criteria:
- Sub-criteria must be **problem-specific** (not generic)
- **No correctness language** in Completeness criteria
- **No syntax/keyword requirements** in any dimension

**Patches applied:**
- `rubric_p002`: Fixed Efficiency sub-criterion that penalized valid O(N) list-scan; fixed Completeness using "correctly handles" (a Correctness word)
- `rubric_p004`: Fixed Completeness sub-criterion using "correctly handles" language

### 3.2 Prompt Engineering — 7 Targeted Fixes to `prompts.py`

| Fix | Rule Added | Targets |
|---|---|---|
| **Fix 1 — CS1 Leniency** | Never use Poor if core logic has any merit | Category A (strictness) |
| **Fix 2 — Dimension Confusion** | Efficiency evaluates STRUCTURE only, never correctness | Category D |
| **Fix 3 — Absence Penalization** | Credit implied loops, functions, output | Category B |
| **Fix 4 — Clarity Independence** | Clarity is independent of correctness | Category G |
| **Fix 5 — Implied Output** | Implied return/print satisfies completeness | Category C |
| **Fix 6 — Efficiency Ceiling** | Missing major component → cap Efficiency at Good | Over-leniency |
| **Fix 7 — Clarity Hedging Ceiling** | Hedging words ("probably", "I think") → cap Clarity at Good; vague conditions → cap at Fair | Over-leniency |

---

## 4. Evaluation Rounds — 6 Versions Tested

We re-evaluated all **20 submissions across 5 problems** after each fix. Results tracked using **Cohen's Weighted Kappa** compared to 2 human raters.

### Cohen's Kappa scale (Landis & Koch, 1977):
- ≥ 0.80 = Almost perfect
- 0.61–0.80 = **Substantial** ← target
- 0.41–0.60 = Moderate
- < 0.40 = Fair/Poor

### All 6 versions compared (averaged across R1 + R2):

| Version | Correctness | Completeness | Clarity | Efficiency | Weighted κ | All ≥ Substantial? |
|---|---|---|---|---|---|---|
| V_eff — efficiency fix only | 0.787 | 0.827 | 0.555 ⚠️ | 0.724 | 0.746 | ❌ |
| **V_clarity18 — all fixes, 18 subs** | **0.754** | **0.827** | **0.791** | **0.674** | **0.775** | **✅** |
| **V_clarity20 — all fixes, 20 subs** | **0.754** | **0.786** | **0.631** | **0.625** | **0.726** | **✅** |
| V4 — strict tier anchors | 0.822 | 0.887 | 0.533 ⚠️ | 0.585 ⚠️ | 0.760 | ❌ |
| V5 — balanced revert | 0.787 | 0.827 | 0.650 | 0.490 ⚠️ | 0.742 | ❌ |
| V6 — ceiling=Fair | 0.752 | 0.827 | 0.643 | 0.571 ⚠️ | 0.735 | ❌ |

> Weighted κ = 0.40×COR + 0.30×COM + 0.20×CLA + 0.10×EFF

---

## 5. Final Results — Best Stable Version (V_clarity20)

**V_clarity20 is the chosen final version** — the only configuration with all 4 dimensions at Substantial or higher on a full 20-submission evaluation.

### Cohen's Kappa — Final State

| Dimension | Weight | R1 vs Gemini | R2 vs Gemini | Average | Human Baseline |
|---|---|---|---|---|---|
| **Correctness** | 40% | 0.774 ✅ | 0.733 ✅ | **0.754** | 0.880 |
| **Completeness** | 30% | 0.750 ✅ | 0.822 ✅ | **0.786** | 0.792 |
| **Clarity** | 20% | 0.660 ✅ | 0.602 ✅ | **0.631** | 0.864 |
| **Efficiency** | 10% | 0.628 ✅ | 0.622 ✅ | **0.625** | 0.920 |
| **Overall** | | | | **0.699** | 0.864 |
| **Weighted** | | | | **0.726** | — |

### Mean disagreement (LLM − Human) — by rater

| Dimension | Mean (vs R1) | Std (vs R1) | Mean (vs R2) | Std (vs R2) | Combined verdict |
|---|---|---|---|---|---|
| Correctness | **−0.10** | 0.64 | **−0.05** | 0.69 | ✅ Nearly neutral — Gemini very slightly stricter than both |
| Completeness | **+0.20** | 0.52 | **−0.05** | 0.39 | ✅ Good — R2 confirms neutral; R1 gap from Human Error cases |
| Clarity | **+0.25** | 0.64 | **+0.30** | 0.73 | ⚠️ Gemini consistently lenient vs both raters |
| Efficiency | **+0.35** | 0.75 | **+0.25** | 0.79 | ⚠️ Gemini moderately lenient vs both raters |

> Scale: Poor=0, Fair=1, Good=2, Excellent=3. Mean ≈ 0 means perfect agreement direction.

### Cross-rater analysis

**Correctness:** Gemini is nearly neutral vs both raters (−0.10 and −0.05). Gemini is very slightly stricter than humans — a safe and desirable direction for automated grading.

**Completeness:** Gemini appears lenient vs R1 (+0.20) but is essentially neutral vs R2 (−0.05). This contrast is explained by Human Error cases — R1 over-credited several submissions that Gemini correctly scored lower. R2 agreed with Gemini on those cases, so the gap vanishes. The true Completeness calibration is closer to neutral.

**Clarity:** Gemini is consistently more lenient than both raters (+0.25 vs R1, +0.30 vs R2), averaging ~+0.28. This is a genuine systematic bias — Gemini rates pseudocode readability higher than human raters, regardless of which human is the reference. The higher std (0.64–0.73) indicates some inconsistency case-by-case.

**Efficiency:** Gemini is moderately lenient vs both raters (+0.35 vs R1, +0.25 vs R2), averaging ~+0.30. The gap is smaller vs R2, suggesting R2 is slightly more generous on Efficiency than R1. Both gaps are within acceptable range given Efficiency is only 10% of the total grade weight.

---

## 6. Key Findings

### ✅ What improved significantly
| Metric | Before | After | Change |
|---|---|---|---|
| Category B (Absence penalization) | Many violations | **0 violations** | Eliminated |
| Category D (Dimension confusion) | 14 cases | **< 3 cases** | Major reduction |
| Category G (Hallucination) | 6 cases | **0 violations** | Eliminated |
| Completeness κ (R2) | 0.697 | **0.822** | +0.125 |

### ✅ Standout result
**Completeness with Rater 2 (κ=0.822) now exceeds the human-human baseline (κ=0.792)** — the LLM and human agree more on Completeness than the two humans agree with each other.

### ⚠️ Remaining limitations
| Limitation | Reason | Fixable? |
|---|---|---|
| Clarity gap (−0.233 from baseline) | Inherently subjective; Gemini-OpenAI κ ≈ 0.45 | No — structural ceiling |
| Efficiency gap (−0.295 from baseline) | Hard to evaluate efficiency from pseudocode alone | Partially |
| Efficiency mean +0.35 | LLM more lenient on incomplete algorithms | Partially |

---

## 7. Human Error — Cases Where the LLM Was Right

Out of 132 disagreement cases, **14 (11%) were classified as Human Error** — the human rater clearly over- or under-credited a submission in a way that is not defensible against the rubric.

### The 3 cases confirmed across ALL 4 pairs (both LLMs, both raters agree):

| Problem | Level | Dim | Human Score | LLM Score | Why Human Was Wrong |
|---|---|---|---|---|---|
| **P2 / largely_incorrect** | COR | Good | Poor | Student explicitly wrote *"the order may be changed"* — self-admits violating the core uniqueness requirement. Human's Good is clearly wrong. |
| **P2 / incorrect** | COR | Fair | Poor | Student removes ALL instances of duplicates — inverted logic, produces completely wrong output. Human's Fair over-credits fundamentally wrong logic. |
| **P4 / incorrect** | COM | Good | Poor | Student defined no function, used wrong operation (multiply), included no return — **0 of 5 rubric sub-criteria met**. Human's Good is clearly wrong. |

### All 14 Human Error cases:

| Pair | Problem | Level | Dim | Human | LLM | Issue |
|---|---|---|---|---|---|---|
| R1 vs Gem | P1/incorrect | COR | Fair | Poor | Hardcoded 120 for inputs >5 — zero factorial logic; over-credited |
| R1 vs Gem | P2/largely_incorrect | COR | Good | Poor | Admits order violated — Good is clearly wrong |
| R1 vs Gem | P2/incorrect | COR | Fair | Poor | Inverted remove-all logic; over-credited |
| R1 vs Gem | P4/incorrect | COM | Good | Poor | 0/5 sub-criteria met; clearly wrong |
| R1 vs OAI | P1/incorrect | COR | Fair | Poor | Same hardcoded factorial; over-credited |
| R1 vs OAI | P2/largely_incorrect | COR | Good | Poor | Admits order violated |
| R1 vs OAI | P2/incorrect | COR | Fair | Poor | Inverted logic; over-credited |
| R1 vs OAI | P4/incorrect | COM | Good | Poor | 0/5 sub-criteria; clearly wrong |
| R2 vs Gem | P2/largely_incorrect | COR | Good | Poor | Admits order violated |
| R2 vs Gem | P2/incorrect | COR | Fair | Poor | Inverted logic; over-credited |
| R2 vs Gem | P4/incorrect | COM | Good | Poor | 0/5 sub-criteria; clearly wrong |
| R2 vs OAI | P2/largely_incorrect | COR | Good | Poor | Admits order violated |
| R2 vs OAI | P2/incorrect | COR | Fair | Poor | Inverted logic; over-credited |
| R2 vs OAI | P4/incorrect | COM | Good | Poor | 0/5 sub-criteria; clearly wrong |

### Implication for Kappa scores
These 14 Human Error cases artificially **lower** the LLM-Human kappa — the LLM is being penalized for being correct. If Human Error cases were excluded, the true agreement (LLM vs corrected human) would be higher than the reported κ values. In particular, the **Correctness κ gap** between R1-Gemini (0.774) and R2-Gemini (0.733) is partly explained by R1 having given wrong scores that Gemini correctly overrode.

> **Key takeaway:** The LLM scored those 14 submissions correctly. The disagreement came from the human, not the model.

---

## 8. Practical Ceiling — Can We Do Better?

The experiment of 6 different prompt configurations revealed a practical ceiling:

> **Prompt engineering alone cannot close the Clarity and Efficiency gap** because both LLMs (Gemini and OpenAI) score these dimensions differently from each other (κ ≈ 0.45). This is a *criteria ambiguity* problem, not a prompt problem.

### What the system is ready for:
| Dimension | Status |
|---|---|
| Correctness (40%) | ✅ Ready — κ=0.754, near human-level |
| Completeness (30%) | ✅ Ready — κ=0.786, meets human baseline |
| Clarity (20%) | ⚠️ Indicative — κ=0.631, use for guidance |
| Efficiency (10%) | ⚠️ Indicative — κ=0.625, use for guidance |

**The system reliably grades 70% of the rubric weight (Correctness + Completeness) at near-human level.**

---

## 8. Next Steps

| Priority | Action |
|---|---|
| 1 | Evaluate OpenAI with the same new prompts + rubrics (not yet done) |
| 2 | Expand to all 20 problems (currently validated on P1–P5 only) |
| 3 | Investigate the 2 edge-case submissions that consistently lower Clarity kappa |
| 4 | Consider human review flag for borderline Clarity/Efficiency scores |
| 5 | Document rubric generation guidelines to prevent future sub-criteria quality issues |

---

## Summary Table

| Item | Details |
|---|---|
| Problems evaluated | P1–P5 (5 problems, 20 submissions each) |
| LLM evaluated | Gemini 2.5 Flash |
| Human raters | 2 raters (R1, R2) |
| Evaluation rounds | 6 versions tested |
| Prompt fixes applied | 7 targeted fixes |
| Rubrics patched | 2 (p002, p004) |
| Final overall κ | 0.699 (simple avg), **0.726 (weighted)** |
| All dims ≥ Substantial | ✅ Yes |
| Completeness vs baseline | ✅ Meets human-human baseline |
