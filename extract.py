import json

with open("itds120-final-q4_with_pseudocode.json", "r", encoding="utf-8") as file:
    data = json.load(file)

extracted = []

for item in data:
    extracted.append({
        "User ID": item["User ID"],
        "Pseudocode": item["Pseudocode"]
    })

with open("final-q4_with_pseudocode.json", "w", encoding="utf-8") as file:
    json.dump(extracted, file, ensure_ascii=False, indent=2)