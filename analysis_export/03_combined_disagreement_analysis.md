# FILE: 03_combined_disagreement_analysis.txt
# DESCRIPTION: Combined cross-rater disagreement analysis (Gemini + OpenAI vs Rater1 + Rater2)
# SOURCE: combined_disagreement_analysis.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Combined Disagreement Analysis — All 4 Pairs
## 132 total cases | Combined framework from both analyses

---

## Category Legend

| Code | Name | Description |
|---|---|---|
| **A** | LLM systematic strictness | LLM scored lower than human; LLM's reasoning is valid but reflects a consistent pattern of being stricter |
| **B** | Absence penalization | LLM penalized for the absence of something (e.g. a variable name, a structural keyword) even though the concept is present |
| **C** | Rubric prescription | A specific rubric sub-criterion caused an unfair penalty that doesn't reflect real learning value |
| **D** | Dimension confusion | A real flaw exists but was charged to the wrong dimension (e.g. a Correctness flaw penalized under Efficiency) |
| **F** | LLM leniency | LLM scored higher than human; LLM was more generous, not always correctly |
| **G** | LLM hallucination | LLM cited an issue that doesn't exist, or gave a score that cannot be justified by the actual pseudocode |
| **HE** | Human error | Human score is clearly wrong — significantly over- or under-crediting logic that is unambiguously correct or wrong |

---

## Pair 1 — R1 vs Gemini (33 cases)

| # | Problem | Level | Dim | Human | Gemini | Cat | Note |
|---|---|---|---|---|---|---|---|
| 1 | P1 | partially_correct | COR | Good | Fair | A | Multiplies from 5 downward — correct direction. Gemini strict about missing explicit loop starting from 1 |
| 2 | P1 | incorrect | COR | Fair | Poor | HE | Student hardcoded 120 for inputs >5, returns number for ≤5 — zero factorial logic present; human over-credited |
| 3 | P2 | partially_correct | COR | Fair | Poor | A | Adjacent-only duplicate check — real flaw, but Gemini gave Poor where human gave Fair for partial logic |
| 4 | P2 | largely_incorrect | COR | Good | Poor | HE | Student wrote "the order may be changed" — self-admits violating core requirement; human's Good is clearly wrong |
| 5 | P2 | incorrect | COR | Fair | Poor | HE | Student removes ALL instances of duplicates — inverted logic, produces wrong output; human's Fair over-credits |
| 6 | P4 | largely_incorrect | COR | Poor | Fair | F | Add then subtract (wrong subtraction), return one value — Gemini gave Fair crediting the addition step |
| 7 | P4 | incorrect | COR | Fair | Poor | A | Multiplies instead of add/subtract — wrong operation; Gemini's Poor is defensible, systematic strictness |
| 8 | P1 | correct | COM | Good | Excellent | F | Full loop algorithm present. Gemini gave Excellent ignoring missing N=0 edge case that rubric requires |
| 9 | P1 | largely_incorrect | COM | Poor | Fair | F | Additive instead of multiplicative but has loop+output structure. Gemini credited structural presence |
| 10 | P2 | correct | COM | Good | Excellent | F | Complete algorithm. Gemini gave Excellent ignoring missing empty-list edge case |
| 11 | P2 | partially_correct | COM | Poor | Fair | B | Has implied loop. Gemini credited loop presence; human penalized because output/seen-list components absent |
| 12 | P3 | correct | COM | Excellent | Good | C | Rubric sub-criterion requires explicit non-letter character filter; student implied it with "spaces and ! are ignored" |
| 13 | P4 | correct | COM | Excellent | Good | C | Rubric sub-criterion requires keyword "FUNCTION calculation(a, b)"; student wrote "the function takes two numbers" |
| 14 | P4 | incorrect | COM | Good | Poor | HE | No function defined, wrong operation (multiply), no return — 0 of 5 sub-criteria met; human's Good is clearly wrong |
| 15 | P1 | partially_correct | CLA | Good | Fair | A | Readable step-by-step multiply from 5 down. Gemini flagged ambiguous variable references ("the number", "it") |
| 16 | P1 | incorrect | CLA | Poor | Excellent | G | Student wrote a clearly wrong hardcoded conditional. Gemini gave Excellent clarity — 3-level gap from human's Poor; hallucination |
| 17 | P2 | partially_correct | CLA | Good | Fair | A | Adjacent-only logic written clearly. Gemini stricter on missing explicit output list and variable names |
| 18 | P2 | incorrect | CLA | Good | Fair | A | Count-occurrences approach described clearly. Gemini strict about missing concrete implementation steps |
| 19 | P3 | partially_correct | CLA | Good | Fair | A | Informal consonant shortcut (sentence_length minus vowels) — readable but vague. Gemini stricter |
| 20 | P3 | largely_incorrect | CLA | Fair | Poor | A | Counts spaces for consonants — clearly written but wrong. Gemini gave Poor; human gave Fair for readability |
| 21 | P3 | incorrect | CLA | Fair | Poor | A | Words as proxy for vowels/consonants — clear sentences but nonsensical logic. Gemini stricter |
| 22 | P4 | partially_correct | CLA | Fair | Good | F | Student says "print it after instead of sending both from the function" — Gemini lenient on print-vs-return confusion |
| 23 | P4 | incorrect | CLA | Fair | Poor | A | Multiplies and prints — clearly stated but wrong approach. Gemini's Poor is consistent with systematic strictness |
| 24 | P1 | partially_correct | EFF | Good | Fair | A | Notes "×1 is unnecessary" — shows efficiency thinking. Gemini penalized for missing generalized loop structure |
| 25 | P2 | correct | EFF | Excellent | Fair | C | P2 rubric explicitly flags O(n²) membership check on output list. Rubric sub-criterion causes this penalty |
| 26 | P2 | partially_correct | EFF | Good | Poor | D | Adjacent-only comparison is O(N) — an efficient operation. The real flaw is Correctness (wrong scope), not Efficiency |
| 27 | P2 | largely_incorrect | EFF | Fair | Poor | C | Sort+scan — P2 rubric specifically penalizes two-pass approaches; rubric sub-criterion is the trigger |
| 28 | P2 | incorrect | EFF | Good | Poor | A | Count+remove — two passes; Gemini's Poor for efficiency is consistent but more strict than human's Good |
| 29 | P3 | partially_correct | EFF | Good | Fair | A | Counts vowels then derives consonants — a reasonable single-pass approach. Gemini stricter |
| 30 | P4 | partially_correct | EFF | Fair | Excellent | G | Incomplete function (subtraction printed separately, not returned) — Gemini gave Excellent efficiency; not justified |
| 31 | P4 | largely_incorrect | EFF | Fair | Excellent | G | Returns only one value — Gemini gave Excellent efficiency to an incomplete, incorrect function; hallucination |
| 32 | P4 | incorrect | EFF | Fair | Poor | A | Wrong operation entirely (multiply). Gemini's Poor for efficiency consistent with systematic strictness |
| 33 | P5 | largely_incorrect | EFF | Fair | Poor | D | Calling function with same value (10) each time is infinite recursion — a Correctness failure (no base case), not an Efficiency flaw |

**Subtotals:** A=14 | B=1 | C=4 | D=2 | F=5 | G=3 | HE=4 | **Total=33**

---

## Pair 2 — R1 vs OpenAI (29 cases)

| # | Problem | Level | Dim | Human | OpenAI | Cat | Note |
|---|---|---|---|---|---|---|---|
| 1 | P1 | partially_correct | COR | Good | Fair | A | Same multiply-from-5 issue. OpenAI stricter about missing generalized loop |
| 2 | P1 | incorrect | COR | Fair | Poor | HE | Hardcoded answer — zero factorial logic; human's Fair is an over-credit |
| 3 | P2 | correct | COR | Excellent | Good | A | Fully correct algorithm, preserves order. OpenAI deducted one tier — systematic strictness |
| 4 | P2 | partially_correct | COR | Fair | Poor | A | Adjacent-only — real flaw but human gave Fair for partial understanding; OpenAI stricter |
| 5 | P2 | largely_incorrect | COR | Good | Poor | HE | Student explicitly admits "the order may be changed" — human's Good is clearly wrong |
| 6 | P2 | incorrect | COR | Fair | Poor | HE | Remove-all-instances logic is fundamentally inverted; human's Fair over-credits |
| 7 | P4 | incorrect | COR | Fair | Poor | A | Multiplies instead of add/subtract — OpenAI's Poor consistent with systematic strictness |
| 8 | P3 | correct | COM | Excellent | Good | C | Rubric requires explicit print/output step at end; student's algorithm implies it but doesn't state it |
| 9 | P4 | correct | COM | Excellent | Good | C | Rubric requires "FUNCTION calculation(a, b)" keyword; student described it in plain language |
| 10 | P4 | incorrect | COM | Good | Poor | HE | No function, wrong operation, no return — 0/5 sub-criteria; human's Good is clearly wrong |
| 11 | P1 | partially_correct | CLA | Good | Fair | A | Readable multiply sequence. OpenAI strict about implicit loop and informal phrasing |
| 12 | P2 | correct | CLA | Excellent | Good | A | Very clear plain-English algorithm. OpenAI deducted for informal list naming |
| 13 | P2 | partially_correct | CLA | Good | Fair | A | Adjacent-only described clearly. OpenAI strict about missing output step and variable names |
| 14 | P2 | largely_incorrect | CLA | Fair | Poor | A | Sort with admitted caveat — readable. OpenAI strict about missing concrete deduplication steps |
| 15 | P2 | incorrect | CLA | Good | Fair | A | Count-occurrences described clearly. OpenAI strict about missing order/result construction |
| 16 | P3 | partially_correct | CLA | Good | Fair | A | Informal consonant shortcut — intent clear, formula vague. OpenAI stricter |
| 17 | P3 | largely_incorrect | CLA | Fair | Poor | A | Counts spaces for consonants — stated plainly but wrong. OpenAI stricter |
| 18 | P4 | partially_correct | CLA | Fair | Good | F | Print-vs-return confusion — OpenAI lenient, found overall function description clear |
| 19 | P4 | incorrect | CLA | Fair | Poor | A | Multiplies and prints — OpenAI's Poor consistent, systematic strictness |
| 20 | P5 | correct | CLA | Excellent | Good | A | Excellent recursive description with base case and accumulation. OpenAI deducted for informal language |
| 21 | P5 | largely_incorrect | CLA | Poor | Fair | F | Infinite loop description — human gave Poor; OpenAI gave Fair for recognizing some recursive intent |
| 22 | P2 | correct | EFF | Excellent | Fair | C | P2 rubric sub-criterion explicitly flags O(n²) membership scan on output list |
| 23 | P2 | partially_correct | EFF | Good | Poor | D | Adjacent comparison is O(N) — efficient. The flaw is Correctness (wrong scope), wrongly charged to Efficiency |
| 24 | P2 | largely_incorrect | EFF | Fair | Poor | C | Sort+scan — P2 rubric specifically penalizes this two-pass pattern |
| 25 | P2 | incorrect | EFF | Good | Poor | A | Count+remove — two passes. OpenAI stricter than human's Good |
| 26 | P4 | partially_correct | EFF | Fair | Good | F | Incomplete function — OpenAI gave Good for efficiency despite missing return of subtraction result |
| 27 | P4 | largely_incorrect | EFF | Fair | Poor | A | Returns only one value — OpenAI's Poor consistent with systematic strictness |
| 28 | P4 | incorrect | EFF | Fair | Poor | A | Wrong operation entirely. OpenAI's Poor consistent |
| 29 | P5 | largely_incorrect | EFF | Fair | Poor | D | Infinite recursion (same arg each call) is a Correctness failure (no base case), not an Efficiency problem |

**Subtotals:** A=16 | B=0 | C=4 | D=2 | F=3 | G=0 | HE=4 | **Total=29**

---

## Pair 3 — R2 vs Gemini (32 cases)

| # | Problem | Level | Dim | Human | Gemini | Cat | Note |
|---|---|---|---|---|---|---|---|
| 1 | P1 | correct | COR | Good | Excellent | F | Full loop algorithm with initialization. Gemini gave Excellent; R2 gave Good (possibly noting implicit base case) |
| 2 | P1 | partially_correct | COR | Good | Fair | A | Multiply from 5 down — correct pattern, not generalized. Gemini stricter |
| 3 | P2 | partially_correct | COR | Fair | Poor | A | Adjacent-only flaw — human gave Fair for partial understanding; Gemini gave Poor for fundamental failure |
| 4 | P2 | largely_incorrect | COR | Good | Poor | HE | Student admits "the order may be changed" — human's Good is clearly wrong given core requirement violation |
| 5 | P2 | incorrect | COR | Fair | Poor | HE | Remove-all-instances = inverted logic; human's Fair over-credits a fundamentally wrong algorithm |
| 6 | P4 | incorrect | COR | Fair | Poor | A | Multiplies instead of add/subtract. Gemini's Poor consistent with systematic strictness |
| 7 | P1 | incorrect | COM | Fair | Poor | A | If/else conditional with hardcoded value — has some structure. Gemini gave Poor; human gave Fair |
| 8 | P3 | correct | COM | Excellent | Good | C | Rubric requires explicit output statement; student's algorithm implies it but doesn't write "print vowels, consonants" |
| 9 | P4 | correct | COM | Excellent | Good | C | Rubric requires "FUNCTION calculation(a, b)" keyword; student described function in plain language |
| 10 | P4 | incorrect | COM | Good | Poor | HE | No function, wrong operation (multiply), no return — 0/5 sub-criteria; human's Good is clearly wrong |
| 11 | P1 | partially_correct | CLA | Good | Fair | A | Readable multiply-from-5 description. Gemini flagged informal variable references |
| 12 | P1 | largely_incorrect | CLA | Poor | Fair | F | Student adds instead of multiplies but states steps clearly. Gemini gave Fair; R2 gave Poor |
| 13 | P1 | incorrect | CLA | Fair | Excellent | G | Clearly wrong hardcoded conditional ("if >5, print 120"). Gemini gave Excellent clarity — 2-level gap; hallucination |
| 14 | P2 | correct | CLA | Good | Excellent | F | Clear plain-English algorithm with all steps. Gemini gave Excellent; R2 gave Good |
| 15 | P2 | partially_correct | CLA | Good | Fair | A | Adjacent-only written clearly. Gemini strict about missing output list mechanism |
| 16 | P2 | incorrect | CLA | Good | Fair | A | Count-occurrences described clearly. Gemini strict about missing concrete steps |
| 17 | P3 | partially_correct | CLA | Good | Fair | A | Informal shortcut for consonants — readable intent. Gemini stricter |
| 18 | P3 | largely_incorrect | CLA | Fair | Poor | A | Counts spaces for consonants — plain sentences but wrong. Gemini stricter |
| 19 | P3 | incorrect | CLA | Fair | Poor | A | Words as vowel/consonant proxy — vague logic. Gemini stricter |
| 20 | P4 | partially_correct | CLA | Fair | Good | F | Print-vs-return confusion — Gemini lenient, found function description understandable |
| 21 | P4 | incorrect | CLA | Fair | Poor | A | Multiplies and prints — Gemini's Poor consistent with systematic strictness |
| 22 | P1 | partially_correct | EFF | Excellent | Fair | A | Notes "×1 is unnecessary" — good efficiency insight. Gemini gave Fair (2-level gap) for missing generalized loop |
| 23 | P2 | correct | EFF | Excellent | Fair | C | P2 rubric sub-criterion explicitly flags O(n²) membership scan on growing output list |
| 24 | P2 | partially_correct | EFF | Good | Poor | D | Adjacent comparison is O(N) — efficient. Wrongly penalized under Efficiency for a Correctness flaw |
| 25 | P2 | largely_incorrect | EFF | Fair | Poor | C | Sort+scan — P2 rubric specifically penalizes this two-pass pattern as inefficient |
| 26 | P2 | incorrect | EFF | Good | Poor | A | Count+remove — two passes. Gemini stricter than human's Good |
| 27 | P3 | partially_correct | EFF | Good | Fair | A | Vowel counting then consonant derivation — single-pass intent. Gemini stricter |
| 28 | P3 | largely_incorrect | EFF | Fair | Poor | A | Two-pass wrong approach (counts all chars, then spaces). Gemini's Poor consistent |
| 29 | P4 | partially_correct | EFF | Fair | Excellent | G | Incomplete function (subtraction printed separately) — Gemini gave Excellent efficiency; not justified |
| 30 | P4 | largely_incorrect | EFF | Fair | Excellent | G | Returns only one value — Gemini gave Excellent efficiency to incorrect, incomplete function; hallucination |
| 31 | P4 | incorrect | EFF | Fair | Poor | A | Wrong operation entirely. Gemini's Poor consistent with systematic strictness |
| 32 | P5 | largely_incorrect | EFF | Fair | Poor | D | Calling function with same arg (10) each time = infinite recursion, a Correctness failure (no base case), not Efficiency |

**Subtotals:** A=16 | B=0 | C=4 | D=2 | F=4 | G=3 | HE=3 | **Total=32**

---

## Pair 4 — R2 vs OpenAI (38 cases)

| # | Problem | Level | Dim | Human | OpenAI | Cat | Note |
|---|---|---|---|---|---|---|---|
| 1 | P1 | correct | COR | Good | Excellent | F | Full correct algorithm. OpenAI gave Excellent; R2 gave Good |
| 2 | P1 | partially_correct | COR | Good | Fair | A | Multiply from 5 — not generalized. OpenAI stricter |
| 3 | P2 | correct | COR | Excellent | Good | A | Fully correct, preserves order. OpenAI deducted one tier — systematic strictness |
| 4 | P2 | partially_correct | COR | Fair | Poor | A | Adjacent-only flaw. OpenAI stricter |
| 5 | P2 | largely_incorrect | COR | Good | Poor | HE | Student admits order violated — human's Good clearly wrong |
| 6 | P2 | incorrect | COR | Fair | Poor | HE | Remove-all-instances = inverted logic; human's Fair over-credits |
| 7 | P4 | largely_incorrect | COR | Fair | Poor | A | Returns only one value (wrong subtraction). OpenAI stricter |
| 8 | P4 | incorrect | COR | Fair | Poor | A | Multiplies instead of add/subtract. OpenAI's Poor consistent |
| 9 | P1 | correct | COM | Excellent | Good | A | Complete algorithm. OpenAI deducted — systematic strictness on edge case sub-criteria |
| 10 | P1 | largely_incorrect | COM | Fair | Poor | A | Has loop-like structure (lists 5 to 1). OpenAI gave Poor; human gave Fair for structural presence |
| 11 | P1 | incorrect | COM | Fair | Poor | A | If/else with output — some structure present. OpenAI stricter |
| 12 | P2 | correct | COM | Excellent | Good | A | Complete algorithm. OpenAI deducted — systematic strictness |
| 13 | P2 | partially_correct | COM | Fair | Poor | A | Adjacent-only — missing seen-tracker and output. OpenAI stricter |
| 14 | P3 | correct | COM | Excellent | Good | C | Rubric requires explicit print statement at end; student implied completion without writing it |
| 15 | P4 | correct | COM | Excellent | Good | C | Rubric requires "FUNCTION calculation(a, b)" keyword; student described function in natural language |
| 16 | P4 | incorrect | COM | Good | Poor | HE | No function, wrong operation, no return — 0/5 sub-criteria; human's Good is clearly wrong |
| 17 | P1 | partially_correct | CLA | Good | Fair | A | Readable multiply sequence. OpenAI strict |
| 18 | P1 | largely_incorrect | CLA | Poor | Fair | F | Adds instead of multiplies but states steps. OpenAI gave Fair; R2 gave Poor |
| 19 | P1 | incorrect | CLA | Fair | Poor | A | Clear hardcoded conditional — readable but wrong. OpenAI stricter |
| 20 | P2 | partially_correct | CLA | Good | Fair | A | Adjacent-only written clearly. OpenAI strict about missing variable names |
| 21 | P2 | largely_incorrect | CLA | Fair | Poor | A | Sort with admitted caveat — readable. OpenAI stricter |
| 22 | P2 | incorrect | CLA | Good | Fair | A | Count-occurrences described clearly. OpenAI strict |
| 23 | P3 | partially_correct | CLA | Good | Fair | A | Informal shortcut — intent clear. OpenAI stricter |
| 24 | P3 | largely_incorrect | CLA | Fair | Poor | A | Counts spaces for consonants — plain but wrong. OpenAI stricter |
| 25 | P4 | partially_correct | CLA | Fair | Good | F | Print-vs-return — OpenAI lenient on function description |
| 26 | P4 | incorrect | CLA | Fair | Poor | A | Multiplies and prints — OpenAI's Poor consistent |
| 27 | P5 | correct | CLA | Excellent | Good | A | Excellent recursive description. OpenAI deducted for informal language |
| 28 | P5 | largely_incorrect | CLA | Poor | Fair | F | Infinite loop — OpenAI gave Fair for recognizing recursive intent; R2 gave Poor |
| 29 | P1 | partially_correct | EFF | Excellent | Good | A | Notes "×1 is unnecessary." OpenAI deducted one tier for missing generalized loop |
| 30 | P2 | correct | EFF | Excellent | Fair | C | P2 rubric sub-criterion flags O(n²) membership scan on output list |
| 31 | P2 | partially_correct | EFF | Good | Poor | D | Adjacent comparison is O(N) — efficient. Correctness flaw (wrong scope) wrongly charged to Efficiency |
| 32 | P2 | largely_incorrect | EFF | Fair | Poor | C | Sort+scan — P2 rubric explicitly penalizes this pattern |
| 33 | P2 | incorrect | EFF | Good | Poor | A | Count+remove two passes. OpenAI stricter |
| 34 | P3 | largely_incorrect | EFF | Fair | Poor | A | Two-pass wrong approach. OpenAI stricter |
| 35 | P4 | partially_correct | EFF | Fair | Good | F | Incomplete function — OpenAI gave Good efficiency despite missing return |
| 36 | P4 | largely_incorrect | EFF | Fair | Poor | A | Returns one value. OpenAI's Poor consistent |
| 37 | P4 | incorrect | EFF | Fair | Poor | A | Wrong operation entirely. OpenAI's Poor consistent |
| 38 | P5 | largely_incorrect | EFF | Fair | Poor | D | Calling function with same arg each time = infinite recursion, a Correctness failure not an Efficiency flaw |

**Subtotals:** A=24 | B=0 | C=4 | D=2 | F=5 | G=0 | HE=3 | **Total=38**

---

## Grand Summary

| Category | R1 vs Gem | R1 vs OAI | R2 vs Gem | R2 vs OAI | **Total** | **%** |
|---|---|---|---|---|---|---|
| **A** LLM systematic strictness | 14 | 16 | 16 | 24 | **70** | **53%** |
| **B** Absence penalization | 1 | 0 | 0 | 0 | **1** | **1%** |
| **C** Rubric prescription | 4 | 4 | 4 | 4 | **16** | **12%** |
| **D** Dimension confusion | 2 | 2 | 2 | 2 | **8** | **6%** |
| **F** LLM leniency | 5 | 3 | 4 | 5 | **17** | **13%** |
| **G** LLM hallucination | 3 | 0 | 3 | 0 | **6** | **5%** |
| **HE** Human error | 4 | 4 | 3 | 3 | **14** | **11%** |
| **Total** | **33** | **29** | **32** | **38** | **132** | **100%** |

---

## Cross-Pair Consistency (Cases in All 4 Pairs)

| Problem | Level | Dim | Human | LLM | Cat | Consistent? |
|---|---|---|---|---|---|---|
| P2 | largely_incorrect | COR | Good | Poor | **HE** | ✅ All 4 pairs |
| P2 | incorrect | COR | Fair | Poor | **HE** | ✅ All 4 pairs |
| P4 | incorrect | COM | Good | Poor | **HE** | ✅ All 4 pairs |
| P3 | correct | COM | Excellent | Good | **C** | ✅ All 4 pairs |
| P4 | correct | COM | Excellent | Good | **C** | ✅ All 4 pairs |
| P2 | correct | EFF | Excellent | Fair | **C** | ✅ All 4 pairs |
| P2 | partially_correct | EFF | Good | Poor | **D** | ✅ All 4 pairs |
| P2 | largely_incorrect | EFF | Fair | Poor | **C** | ✅ All 4 pairs |
| P5 | largely_incorrect | EFF | Fair | Poor | **D** | ✅ All 4 pairs |
| P4 | incorrect | COR | Fair | Poor | **A** | ✅ All 4 pairs |
| P2 | partially_correct | COR | Fair/Good | Poor | **A** | ✅ All 4 pairs |
| P3 | partially_correct | CLA | Good | Fair | **A** | ✅ All 4 pairs |
| P3 | largely_incorrect | CLA | Fair | Poor | **A** | ✅ All 4 pairs |
