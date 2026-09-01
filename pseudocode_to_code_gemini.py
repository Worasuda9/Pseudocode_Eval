import json
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please add it to your .env file.")

client = OpenAI(api_key=api_key)

INPUT_FILE = "final-q4_with_pseudocode.json"
OUTPUT_FILE = "final-q4_pseudocode_to_code_gemini.json"


def convert_pseudocode_to_python(pseudocode):
    prompt = f"""
Can you change this pseudocode into Python code?

Requirements:
- Output only Python code.
- Do not include explanation.
- Do not use markdown code block.
- Make the code easy to read.
- Keep the same logic as the pseudocode.

Pseudocode:
{pseudocode}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

for index, item in enumerate(data, start=1):
    user_id = item.get("User ID")
    pseudocode = item.get("Pseudocode", "")

    print(f"Processing {index}/{len(data)} | User ID: {user_id}")

    try:
        python_code = convert_pseudocode_to_python(pseudocode)

        item["Pseudocode to Code"] = python_code

    except Exception as e:
        item["Pseudocode to Code"] = ""
        item["Error"] = str(e)

    time.sleep(0.5)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"Done! Created {OUTPUT_FILE}")