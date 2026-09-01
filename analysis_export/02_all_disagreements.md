# FILE: 02_all_disagreements.txt
# DESCRIPTION: Full listing of every disagreement case with category classification
# SOURCE: all_disagreements.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Complete Disagreement Case Listing — All 4 Pairs
**All individual disagreements identified and categorized**

Category key: **RP** = Rubric prescription | **DC** = Dimension confusion | **LD** = Legitimate disagreement | **HE** = Human error | **LH** = LLM hallucination

---

## Pair 1 — rater1 vs Gemini (31 disagreements)

| # | Problem | Level | Dimension | Human | Gemini | Category |
|---|---|---|---|---|---|---|
| 1 | P1 | correct | Completeness | Good | Excellent | LD |
| 2 | P1 | partially_correct | Correctness | Good | Fair | LD |
| 3 | P1 | partially_correct | Clarity | Good | Fair | LD |
| 4 | P1 | partially_correct | Efficiency | Good | Fair | RP |
| 5 | P1 | largely_incorrect | Completeness | Poor | Fair | LD |
| 6 | P1 | incorrect | Correctness | Fair | Poor | HE |
| 7 | P1 | incorrect | Clarity | Poor | Excellent | LD |
| 8 | P2 | correct | Completeness | Good | Excellent | LD |
| 9 | P2 | correct | Efficiency | Excellent | Fair | RP |
| 10 | P2 | partially_correct | Correctness | Fair | Poor | LD |
| 11 | P2 | partially_correct | Completeness | Poor | Fair | LD |
| 12 | P2 | partially_correct | Clarity | Good | Fair | LD |
| 13 | P2 | partially_correct | Efficiency | Good | Poor | DC |
| 14 | P2 | largely_incorrect | Correctness | Good | Poor | HE |
| 15 | P2 | largely_incorrect | Efficiency | Fair | Poor | LD |
| 16 | P2 | incorrect | Correctness | Fair | Poor | HE |
| 17 | P2 | incorrect | Clarity | Good | Fair | LD |
| 18 | P2 | incorrect | Efficiency | Good | Poor | DC |
| 19 | P3 | correct | Completeness | Excellent | Good | RP |
| 20 | P3 | partially_correct | Clarity | Good | Fair | LD |
| 21 | P3 | partially_correct | Efficiency | Good | Fair | DC |
| 22 | P3 | largely_incorrect | Clarity | Fair | Poor | LD |
| 23 | P3 | incorrect | Clarity | Fair | Poor | LD |
| 24 | P4 | correct | Completeness | Excellent | Good | RP |
| 25 | P4 | partially_correct | Clarity | Fair | Good | LD |
| 26 | P4 | partially_correct | Efficiency | Fair | Excellent | LD |
| 27 | P4 | largely_incorrect | Correctness | Poor | Fair | LD |
| 28 | P4 | largely_incorrect | Efficiency | Fair | Excellent | LD |
| 29 | P4 | incorrect | Correctness | Fair | Poor | HE |
| 30 | P4 | incorrect | Completeness | Good | Poor | HE |
| 31 | P4 | incorrect | Clarity | Fair | Poor | LD |
| 32 | P4 | incorrect | Efficiency | Fair | Poor | DC |
| 33 | P5 | largely_incorrect | Efficiency | Fair | Poor | DC |

**Pair 1 subtotals:** RP=4 | DC=5 | LD=17 | HE=5 | LH=0 | **Total=31**

---

## Pair 2 — rater1 vs OpenAI (27 disagreements)

| # | Problem | Level | Dimension | Human | OpenAI | Category |
|---|---|---|---|---|---|---|
| 1 | P1 | partially_correct | Correctness | Good | Fair | LD |
| 2 | P1 | partially_correct | Clarity | Good | Fair | LD |
| 3 | P1 | incorrect | Correctness | Fair | Poor | HE |
| 4 | P2 | correct | Correctness | Excellent | Good | DC |
| 5 | P2 | correct | Clarity | Excellent | Good | RP |
| 6 | P2 | correct | Efficiency | Excellent | Fair | LD |
| 7 | P2 | partially_correct | Correctness | Fair | Poor | LD |
| 8 | P2 | partially_correct | Clarity | Good | Fair | LD |
| 9 | P2 | partially_correct | Efficiency | Good | Poor | DC |
| 10 | P2 | largely_incorrect | Correctness | Good | Poor | HE |
| 11 | P2 | largely_incorrect | Clarity | Fair | Poor | LD |
| 12 | P2 | largely_incorrect | Efficiency | Fair | Poor | LD |
| 13 | P2 | incorrect | Correctness | Fair | Poor | HE |
| 14 | P2 | incorrect | Clarity | Good | Fair | LD |
| 15 | P2 | incorrect | Efficiency | Good | Poor | LH |
| 16 | P3 | correct | Completeness | Excellent | Good | RP |
| 17 | P3 | partially_correct | Clarity | Good | Fair | LD |
| 18 | P3 | largely_incorrect | Clarity | Fair | Poor | LD |
| 19 | P4 | correct | Completeness | Excellent | Good | RP |
| 20 | P4 | partially_correct | Clarity | Fair | Good | LD |
| 21 | P4 | partially_correct | Efficiency | Fair | Good | LD |
| 22 | P4 | largely_incorrect | Efficiency | Fair | Poor | LH |
| 23 | P4 | incorrect | Correctness | Fair | Poor | HE |
| 24 | P4 | incorrect | Completeness | Good | Poor | HE |
| 25 | P4 | incorrect | Clarity | Fair | Poor | LD |
| 26 | P5 | correct | Clarity | Excellent | Good | RP |
| 27 | P5 | largely_incorrect | Clarity | Poor | Fair | LD |
| 28 | P5 | largely_incorrect | Efficiency | Fair | Poor | LD |

**Pair 2 subtotals:** RP=4 | DC=2 | LD=13 | HE=6 | LH=2 | **Total=27**

---

## Pair 3 — rater2 vs Gemini (28 disagreements)

| # | Problem | Level | Dimension | Human | Gemini | Category |
|---|---|---|---|---|---|---|
| 1 | P1 | correct | Correctness | Good | Excellent | LD |
| 2 | P1 | partially_correct | Correctness | Good | Fair | LD |
| 3 | P1 | partially_correct | Clarity | Good | Fair | RP |
| 4 | P1 | partially_correct | Efficiency | Excellent | Fair | RP |
| 5 | P1 | largely_incorrect | Clarity | Poor | Fair | LD |
| 6 | P1 | incorrect | Completeness | Fair | Poor | LD |
| 7 | P1 | incorrect | Clarity | Fair | Excellent | HE |
| 8 | P2 | correct | Clarity | Good | Excellent | LD |
| 9 | P2 | correct | Efficiency | Excellent | Fair | DC |
| 10 | P2 | partially_correct | Correctness | Fair | Poor | LD |
| 11 | P2 | partially_correct | Clarity | Good | Fair | LD |
| 12 | P2 | partially_correct | Efficiency | Good | Poor | DC |
| 13 | P2 | largely_incorrect | Correctness | Good | Poor | HE |
| 14 | P2 | largely_incorrect | Efficiency | Fair | Poor | LD |
| 15 | P2 | incorrect | Correctness | Fair | Poor | HE |
| 16 | P2 | incorrect | Clarity | Good | Fair | LD |
| 17 | P2 | incorrect | Efficiency | Good | Poor | DC |
| 18 | P3 | correct | Completeness | Excellent | Good | RP |
| 19 | P3 | largely_incorrect | Clarity | Fair | Poor | LD |
| 20 | P3 | incorrect | Clarity | Fair | Poor | LD |
| 21 | P4 | correct | Completeness | Excellent | Good | RP |
| 22 | P4 | partially_correct | Clarity | Fair | Good | LD |
| 23 | P4 | partially_correct | Efficiency | Fair | Excellent | LD |
| 24 | P4 | largely_incorrect | Efficiency | Fair | Excellent | LD |
| 25 | P4 | incorrect | Correctness | Fair | Poor | HE |
| 26 | P4 | incorrect | Completeness | Good | Poor | HE |
| 27 | P4 | incorrect | Clarity | Fair | Poor | LD |
| 28 | P5 | largely_incorrect | Efficiency | Fair | Poor | DC |

**Pair 3 subtotals:** RP=4 | DC=4 | LD=14 | HE=6 | LH=0 | **Total=28**

---

## Pair 4 — rater2 vs OpenAI (28 disagreements)

| # | Problem | Level | Dimension | Human | OpenAI | Category |
|---|---|---|---|---|---|---|
| 1 | P1 | correct | Correctness | Good | Excellent | HE |
| 2 | P1 | correct | Completeness | Excellent | Good | RP |
| 3 | P1 | partially_correct | Clarity | Good | Fair | LD |
| 4 | P1 | largely_incorrect | Completeness | Fair | Poor | LD |
| 5 | P1 | incorrect | Completeness | Fair | Poor | HE |
| 6 | P1 | incorrect | Clarity | Fair | Poor | LD |
| 7 | P2 | correct | Correctness | Excellent | Good | DC |
| 8 | P2 | correct | Efficiency | Excellent | Fair | LD |
| 9 | P2 | partially_correct | Correctness | Fair | Poor | LD |
| 10 | P2 | partially_correct | Completeness | Fair | Poor | LD |
| 11 | P2 | partially_correct | Efficiency | Good | Poor | DC |
| 12 | P2 | largely_incorrect | Correctness | Good | Poor | HE |
| 13 | P2 | largely_incorrect | Clarity | Fair | Poor | LD |
| 14 | P2 | largely_incorrect | Efficiency | Fair | Poor | LD |
| 15 | P2 | incorrect | Correctness | Fair | Poor | HE |
| 16 | P2 | incorrect | Efficiency | Good | Poor | RP |
| 17 | P3 | correct | Completeness | Excellent | Good | RP |
| 18 | P3 | partially_correct | Clarity | Good | Fair | LD |
| 19 | P3 | largely_incorrect | Clarity | Fair | Poor | LD |
| 20 | P4 | correct | Completeness | Excellent | Good | RP |
| 21 | P4 | partially_correct | Clarity | Fair | Good | LD |
| 22 | P4 | partially_correct | Efficiency | Fair | Good | LD |
| 23 | P4 | largely_incorrect | Correctness | Fair | Poor | LD |
| 24 | P4 | largely_incorrect | Efficiency | Fair | Poor | RP |
| 25 | P4 | incorrect | Correctness | Fair | Poor | HE |
| 26 | P4 | incorrect | Completeness | Good | Poor | HE |
| 27 | P4 | incorrect | Clarity | Fair | Poor | LD |
| 28 | P5 | correct | Clarity | Excellent | Good | RP |
| 29 | P5 | largely_incorrect | Clarity | Poor | Fair | LD |
| 30 | P5 | largely_incorrect | Efficiency | Fair | Poor | LD |

**Pair 4 subtotals:** RP=6 | DC=2 | LD=14 | HE=6 | LH=0 | **Total=28**

---

## Grand Total Across All 4 Pairs

| Category | Pair 1 (r1 vs Gem) | Pair 2 (r1 vs OAI) | Pair 3 (r2 vs Gem) | Pair 4 (r2 vs OAI) | **Total** | **%** |
|---|---|---|---|---|---|---|
| Rubric prescription (RP) | 4 | 4 | 4 | 6 | **18** | **16%** |
| Dimension confusion (DC) | 5 | 2 | 4 | 2 | **13** | **12%** |
| Legitimate disagreement (LD) | 17 | 13 | 14 | 14 | **58** | **52%** |
| Human error (HE) | 5 | 6 | 6 | 6 | **23** | **21%** |
| LLM hallucination (LH) | 0 | 2 | 0 | 0 | **2** | **2%** |
| **Total** | **31** | **27** | **28** | **28** | **114** | **100%** |

---

## Cross-Pair Consistency: Cases That Appear in Multiple Pairs

These disagreements were found in **3 or 4 of the 4 pairs**, making them the most systematic and reliable findings.

| Problem | Level | Dimension | Appears in | Category (consistent?) |
|---|---|---|---|---|
| P2 | largely_incorrect | Correctness | All 4 pairs | HE in all — human gave "Good" to algorithm that destroys order |
| P2 | incorrect | Correctness | All 4 pairs | HE in all — human gave "Fair" to fundamentally wrong logic |
| P4 | incorrect | Correctness | All 4 pairs | HE in all — human gave "Fair" to multiplication instead of add/subtract |
| P4 | incorrect | Completeness | All 4 pairs | HE in all — human gave "Good" with 0/5 sub-criteria met |
| P3 | correct | Completeness | All 4 pairs | RP in all — downgraded for no explicit print statement |
| P4 | correct | Completeness | All 4 pairs | RP in all — downgraded for no "FUNCTION" keyword |
| P2 | partially_correct | Efficiency | All 4 pairs | DC in all — Correctness flaw (adjacent-only) charged to Efficiency |
| P2 | correct | Efficiency | 3 of 4 pairs (r1-Gem, r1-OAI, r2-Gem) | RP/LD — O(N²) penalty for implicit list-scan not stated in pseudocode |
| P4 | incorrect | Clarity | 3 of 4 pairs | LD — readable wrong pseudocode (multiply+print) |
| P5 | correct | Clarity | 2 of 4 pairs (r1-OAI, r2-OAI) | RP — OpenAI only; informal language penalized |
| P5 | largely_incorrect | Efficiency | 2 of 4 pairs (r1-OAI, r2-Gem) | DC — infinite recursion charged to Efficiency |
| P1 | incorrect | Correctness | 2 of 4 pairs (r1-Gem, r1-OAI) | HE — hardcoded value given Fair |
| P1 | incorrect | Clarity | 2 of 4 pairs (r1-Gem, r2-Gem) | LD (Gemini gave Excellent, human gave Poor/Fair) |
