# FILE: 08_prompts_audit_jul17.txt
# DESCRIPTION: Prompt audit after July 17 refactoring (per-dimension architecture)
# SOURCE: prompts_audit_jul17.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# prompts.py Audit Report
## July 17, 2026

---

## Overall Verdict

The prompt is **mostly solid but has one critical contradiction** and three minor issues. The overall architecture is good — the shared `_DIMENSION_DEFINITIONS` as a single source of truth is excellent design. But the V4 strict tier anchors introduced a direct conflict with the lenient qualitative scoring scale that was written for V_clarity20 and never updated.

---

## Issue 1 — CRITICAL: Direct Contradiction on Correctness Excellent

**Severity: 🔴 Critical — model receives contradictory instructions**

The model is told two opposite things about what "Excellent" means for Correctness:

**Qualitative scoring scale (line 246–249) — LENIENT:**
> *"Excellent: fully satisfies the core algorithm logic. For CS1 students, missing edge cases (like empty lists or N=0) alone do not prevent Excellent if the main logic is sound."*

**Performance tier Excellent (line 326–327) — STRICT (V4):**
> *"Correctness: Algorithm produces perfectly correct results for ALL valid inputs and edge cases."*

**Additional evaluator notes (line 273–279) — LENIENT:**
> *"For CS1 students, missing edge cases alone should not prevent an Excellent score on any dimension if the core algorithm logic is sound."*

**Summary:** Two sections say lenient (missing edge cases → still Excellent). One section says strict (ALL edge cases required). The model is getting 2-vs-1 contradictory signals on the most important dimension (40% weight).

**Why this matters:** This is exactly the tension that drove our experiments. The strict tier is V4's key improvement, but the old lenient scoring scale was never updated to match. When the model tries to reconcile these, it may fall back to the lenient interpretation some of the time — causing inconsistent Correctness scores.

**Fix:** Update the qualitative scoring scale for "Excellent" to match V4's strict tier:

```
BEFORE (line 246–249):
"Excellent": fully satisfies the core algorithm logic. For CS1 students,
missing edge cases (like empty lists or N=0) alone do not prevent Excellent
if the main logic is sound. Minor informal naming or wording does not prevent Excellent.

AFTER:
"Excellent": the algorithm produces correct results for all valid inputs and
edge cases defined in the rubric. All structural components are present and
the logic is sound.
```

---

## Issue 2 — MODERATE: Leftover Blank Lines (Lines 291–294)

**Severity: 🟡 Moderate — cosmetic but creates an incomplete appearance**

Lines 291–294 are four consecutive blank lines left over from when the three FIX blocks were deleted. This does not affect the model's behavior significantly (LLMs ignore whitespace), but it:
- Makes the prompt look unfinished
- Could confuse a human reading the file
- Slightly inflates the token count

**Fix:** Delete the four blank lines between the additional notes section and the Critical rules section.

---

## Issue 3 — MINOR: "explicitly" in Completeness Excellent Tier

**Severity: 🟢 Minor — inconsistent terminology**

Line 328–329:
> *"Completeness: Every structural component and edge case **explicitly** defined in the rubric is present."*

The rubric generator is told (line 142–144):
> *"Never use the word 'explicitly' in sub-criteria — it causes natural language pseudocode to be unfairly penalized."*

The context is different — the evaluator's tier uses "explicitly defined in the rubric" (referring to what the rubric contains, not how the student writes it). So it is not the same as requiring explicit syntax from students. But it is still inconsistent terminology and could subtly signal to the model that only formally-written components count.

**Fix:** Change to *"Every structural component and edge case defined in the rubric is present."*

---

## Issue 4 — MINOR: Efficiency Poor — Two Different Definitions

**Severity: 🟢 Minor — two sections define Poor differently**

**Additional evaluator notes (lines 282–284):**
> *"Only mark Poor on Efficiency if there is a clear algorithmic inefficiency (e.g. nested loop where one loop suffices) **OR** if the submission has no algorithmic content at all."*

**Performance tier Poor (lines 360–361):**
> *"Efficiency: No algorithmic content present to evaluate, or the approach would fail to terminate."*

The additional notes say a clear algorithmic inefficiency (e.g. a nested loop) can cause Poor. The tier says Poor is only for completely absent content or infinite termination. These give different signals about when to assign Poor on Efficiency.

**Fix:** Align the additional notes with the tier description, since the tier is the anchor:

```
BEFORE (line 282–284):
Only mark Poor on Efficiency if there is a clear algorithmic inefficiency
(e.g. nested loop where one loop suffices) or if the submission has no
algorithmic content at all.

AFTER:
Only mark Poor on Efficiency if the submission has no algorithmic steps to
evaluate, or if the described approach would never terminate. A correct
algorithm that uses a suboptimal but functional approach should not receive Poor.
```

---

## What Is Working Well

| Element | Assessment |
|---|---|
| `_DIMENSION_DEFINITIONS` as shared source | ✅ Excellent architecture — single source of truth for both prompts |
| Edge case ownership rule (lines 273–279) | ✅ Clear and well-placed in evaluator |
| Structural trace requirement (sequence/branch/loop/termination) | ✅ Very effective — grounds reasoning in actual logic |
| Hint quality guide (lines 312–321) | ✅ The good vs bad examples are concrete and useful |
| JSON schema (lines 363–380) | ✅ Complete and unambiguous |
| RETRY_ADDENDUM (lines 396–406) | ✅ Fully consistent with main prompt requirements |
| Rubric generator edge case rule (stated twice, lines 130–147) | ✅ Important fix, well reinforced |
| [FIX: Rubric prescription] block | ✅ Clear and targeted — prevents formal syntax requirements |
| No-redundancy rule between Completeness and Correctness (lines 119–125) | ✅ Well-defined separation |

---

## What Is Redundant (But Intentionally So)

These are repeated on purpose — reinforcing important rules is correct:

| Rule | Where repeated | Verdict |
|---|---|---|
| Edge case under Completeness only | Lines 130–134 AND lines 145–147 (rubric generator) | ✅ Intentional double-emphasis |
| Edge case → Completeness in evaluator | Lines 273–279 AND qualitative scoring scale | ✅ Intentional reinforcement |
| Hint requirement | Step 5 + Critical rules + RETRY_ADDENDUM | ✅ Intentional — retry needs to restate it |
| Affirmative language | Rubric generator + Critical rules | ✅ Intentional |

---

## Are the Prompts Good Enough Overall?

**For the rubric generator:** ✅ Yes — very solid. The edge case placement rules, no-explicit-syntax rules, and [FIX: Rubric prescription] block are all well-designed. No significant issues.

**For the evaluator:** ⚠️ Almost — the critical contradiction on Issue 1 needs to be fixed. If the model resolves the contradiction in favor of the lenient scoring scale, it will give Excellent on Correctness too generously. If it resolves in favor of the strict tier, it will be appropriately demanding. The outcome is inconsistent, which hurts reproducibility.

**Are they consistent with each other?** ⚠️ Mostly — the `_DIMENSION_DEFINITIONS` shared injection ensures the rubric generator and evaluator use the same dimension definitions. But the evaluator has the internal contradiction (Issue 1) that creates inconsistency within itself.

---

## Recommended Fixes (Priority Order)

| Priority | Issue | Effort |
|---|---|---|
| 🔴 1 | Fix qualitative scoring scale to match V4 strict tier | 3 lines changed |
| 🟡 2 | Delete 4 blank lines (291–294) | 1 edit |
| 🟢 3 | Remove "explicitly" from Completeness Excellent tier | 1 word removed |
| 🟢 4 | Align Efficiency Poor definition in additional notes with tier | 2 lines changed |
