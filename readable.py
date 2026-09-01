import json

input_file = "final-q4_pseudocode_to_code_gemini.json"
output_file = "final-q4_pseudocode_to_code.json"

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    for field in ["Pseudocode", "Pseudocode to Code"]:
        if field in item and isinstance(item[field], str):
            item[field] = item[field].splitlines()

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        data,
        file,
        ensure_ascii=False,
        indent=4
    )

print(f"Created: {output_file}")