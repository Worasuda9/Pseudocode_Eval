# FILE: 21_study_report_abstract.txt
# DESCRIPTION: Academic abstract summarizing the full internship research
# SOURCE: study_report.md
# PROJECT: Automated Pseudocode Evaluation System
# EXPORTED: 2026-07-29
======================================================================

# Study Report — Research Internship
**Student:** [Your Name]  
**Supervisor:** [Professor Name]  
**Institution:** [University Name]  
**Period:** June 2026 – July 2026

---

## Abstract

This study presents the design, development, and evaluation of an automated pseudocode assessment system for introductory programming courses (CS1), leveraging a large language model (LLM) to evaluate student submissions across four dimensions: Correctness, Completeness, Clarity, and Efficiency. The system consists of two core pipelines — an automatic rubric generation pipeline that produces problem-specific grading criteria from a problem statement, and an evaluation pipeline that generates qualitative scores, diagnostic feedback, and Socratic hints for each submission. To measure reliability, Cohen's Weighted Kappa (κ) was computed by comparing the LLM's evaluations against those of two independent human expert raters across 15 programming problems and 60 student submissions. Through systematic prompt engineering across seven iterative versions, the study found that rubric quality is the primary driver of evaluation accuracy — replacing generic sub-criteria with algorithmically grounded, problem-specific checkpoints improved Completeness agreement by approximately 0.15κ. The final optimized configuration achieved a weighted average inter-rater agreement of κ ≈ 0.677 (Substantial), with Correctness reaching κ = 0.835 (Almost Perfect), Completeness κ = 0.662 (Substantial), Efficiency κ = 0.595 (Moderate–Substantial), and Clarity κ = 0.419 (Moderate). These results demonstrate that LLM-based automated assessment can achieve near-human reliability for objective dimensions such as algorithmic correctness, while subjective dimensions such as clarity remain an open challenge for future work.
