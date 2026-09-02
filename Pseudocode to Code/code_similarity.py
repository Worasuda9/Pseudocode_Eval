import json
import re
import io
import tokenize
import difflib
import csv

# =========================
# 1. File paths
# =========================

CODE_FILE = "itds120-final-q4.json"
PSEUDO_FILE = "final-q4_pseudocode_to_code.json"


# =========================
# 2. Load JSON
# =========================

with open(CODE_FILE, "r", encoding="utf-8") as f:
    code_data = json.load(f)

with open(PSEUDO_FILE, "r", encoding="utf-8") as f:
    pseudo_data = json.load(f)


# =========================
# 3. Clean original code
# =========================

def extract_student_code(code):
    """
    Remove metadata such as:

    USERID
    PASSWORD
    EXERCISEID

    and remove:
    # YOUR CODE GOES HERE
    """

    # Remove metadata block inside '''
    code = re.sub(
        r"^\s*'''[\s\S]*?'''\s*",
        "",
        code,
        count=1
    )

    # Remove placeholder comment
    lines = []

    for line in code.splitlines():

        if line.strip() == "# YOUR CODE GOES HERE":
            continue

        lines.append(line)

    return "\n".join(lines).strip()


# =========================
# 4. Ignore input prompt
# =========================

def remove_input_prompt(code):
    """
    Make these equivalent:

    input()
    input("Enter a value: ")
    input('Enter number: ')
    """

    pattern = r'''input\s*\(\s*(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')\s*\)'''

    return re.sub(
        pattern,
        "input()",
        code
    )


# =========================
# 5. Convert code to tokens
# =========================

def code_to_tokens(code):

    code = remove_input_prompt(code)

    tokens = []

    try:

        token_generator = tokenize.generate_tokens(
            io.StringIO(code).readline
        )

        for token in token_generator:

            # Ignore formatting-related tokens
            if token.type in {
                tokenize.ENDMARKER,
                tokenize.NEWLINE,
                tokenize.NL,
                tokenize.INDENT,
                tokenize.DEDENT,
                tokenize.COMMENT
            }:
                continue

            tokens.append(token.string)

    except (tokenize.TokenError, IndentationError):

        # fallback if code cannot be tokenized
        tokens = re.findall(
            r"[A-Za-z_]\w*|\d+(?:\.\d+)?|"
            r"==|!=|<=|>=|\*\*|//|"
            r"[-+*/%=<>()[\]{},.:]",
            code
        )

    return tokens


# =========================
# 6. Calculate similarity
# =========================

def calculate_similarity(code1, code2):

    tokens1 = code_to_tokens(code1)
    tokens2 = code_to_tokens(code2)

    similarity = difflib.SequenceMatcher(
        None,
        tokens1,
        tokens2
    ).ratio()

    return similarity * 100


# =========================
# 7. Create User ID lookup
# =========================

pseudo_lookup = {}

for item in pseudo_data:

    user_id = str(item["User ID"])

    pseudo_code = "\n".join(
        item["Pseudocode to Code"]
    )

    pseudo_lookup[user_id] = pseudo_code


# =========================
# 8. Compare each User ID
# =========================

results = []

for item in code_data:

    user_id = str(item["User ID"])

    if user_id not in pseudo_lookup:
        print(f"User {user_id} not found")
        continue

    original_code = extract_student_code(
        item["Code"]
    )

    generated_code = pseudo_lookup[user_id]

    similarity = calculate_similarity(
        original_code,
        generated_code
    )

    results.append({
        "User ID": user_id,
        "Similarity (%)": round(similarity, 2),
        "Original Code": original_code,
        "Pseudocode to Code": generated_code
    })


# =========================
# 9. Sort from highest
# =========================

results.sort(
    key=lambda x: x["Similarity (%)"],
    reverse=True
)


# =========================
# 10. Print result
# =========================

for result in results:

    print("=" * 60)

    print("User ID:", result["User ID"])
    print(
        "Similarity:",
        f'{result["Similarity (%)"]}%'
    )

    print("\nOriginal Code:")
    print(result["Original Code"])

    print("\nPseudocode to Code:")
    print(result["Pseudocode to Code"])


# =========================
# 11. Overall statistics
# =========================

scores = [
    result["Similarity (%)"]
    for result in results
]

average = sum(scores) / len(scores)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("Total users:", len(results))
print(f"Average similarity: {average:.2f}%")

print(
    "Similarity >= 90%:",
    sum(score >= 90 for score in scores)
)

print(
    "Similarity >= 80%:",
    sum(score >= 80 for score in scores)
)

print(
    "Exactly 100%:",
    sum(score == 100 for score in scores)
)


# =========================
# 12. Export CSV
# =========================

with open(
    "comparison_result final-q4.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "User ID",
            "Similarity (%)",
            "Original Code",
            "Pseudocode to Code"
        ]
    )

    writer.writeheader()
    writer.writerows(results)

print("\nSaved: comparison_result final-q4.csv")