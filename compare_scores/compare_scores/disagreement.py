import pandas as pd

rater1 = pd.read_csv("new_human2.csv")
rater2 = pd.read_csv("gemini3.5.csv")

# merge on join key
merged = rater1.merge(rater2, on=["problem_id", "model", "level"], 
                      suffixes=("_human", "_llm"))

dimensions = ["correctness", "completeness", "clarity", "efficiency"]

for dim in dimensions:
    disagreements = merged[merged[f"{dim}_human"] != merged[f"{dim}_llm"]].copy()
    disagreements["human_score"] = disagreements[f"{dim}_human"]
    disagreements["llm_score"] = disagreements[f"{dim}_llm"]
    disagreements["dimension"] = dim
    # show problem, level, both scores, and the pseudocode
    print(f"\n=== {dim.upper()} DISAGREEMENTS (new_huma2 vs gemini3.5) ===")
    print(disagreements[["problem_id", "level", "human_score", 
                          "llm_score", "pseudocode_human"]].to_string())
    
score_map = {"Poor": 0, "Fair": 1, "Good": 2, "Excellent": 3}

for dim in dimensions:
    merged[f"{dim}_human_n"] = merged[f"{dim}_human"].map(score_map)
    merged[f"{dim}_llm_n"] = merged[f"{dim}_llm"].map(score_map)
    merged[f"{dim}_diff"] = merged[f"{dim}_llm_n"] - merged[f"{dim}_human_n"]
    
    mean_diff = merged[f"{dim}_diff"].mean()
    std_diff  = merged[f"{dim}_diff"].std()
    print(f"{dim}: mean(LLM - human) = {mean_diff:+.2f},  std = {std_diff:.2f}")
    # positive mean = LLM scores higher than human
    # negative mean = LLM scores lower than human (more strict)
    # high std = LLM is inconsistent relative to human across submissions