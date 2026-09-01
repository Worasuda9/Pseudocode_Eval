import json
import os
import sys
import time

from openai import OpenAI
from openai import (
    AuthenticationError,
    RateLimitError,
    APIStatusError,
    APIConnectionError,
)

from prompt import SYSTEM_PROMPT, create_user_prompt

# ==========================
# API CONFIG
# ==========================

API_KEY = os.environ.get("OPENAI_API_KEY", "")

MODEL_NAME = "gpt-4o-mini"

INPUT_FILE = "itds120-cp4-q4.json"

OUTPUT_FILE = "itds120-cp4-q4_with_pseudocode.json"

MAX_RETRIES = 10


def validate_api_key(client):
    """Check that the API Key actually works before processing all records."""

    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return True

    except AuthenticationError:
        return False

    except Exception:
        # Some other issue (e.g. network) - let it pass through and fail later if needed
        return True


def call_api(client, code):

    retries = 0

    while True:

        try:

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": create_user_prompt(code)}
                ],
                temperature=0
            )

            text = response.choices[0].message.content

            if not text:
                raise Exception("OpenAI did not return pseudocode")

            return text.strip()

        except AuthenticationError:
            # If the API key is invalid, retrying is pointless - stop the whole program
            print("\nInvalid API key. Please check OPENAI_API_KEY and run again.")
            sys.exit(1)

        except RateLimitError as error:
            # Hit the Rate Limit - wait and try again (but with a retry limit)
            retries += 1

            if retries > MAX_RETRIES:
                raise Exception(
                    f"Exceeded max retries ({MAX_RETRIES}) due to rate limit"
                )

            print(f"Rate limit reached. Retry {retries}/{MAX_RETRIES}.")
            print("Waiting 12 seconds before retrying...\n")

            time.sleep(12)

            continue

        except (APIStatusError, APIConnectionError) as error:
            # Server overloaded / temporarily unavailable - wait and try again
            retries += 1

            if retries > MAX_RETRIES:
                raise Exception(
                    f"Exceeded max retries ({MAX_RETRIES}) due to server error: {error}"
                )

            print(f"Server issue ({error}). Retry {retries}/{MAX_RETRIES}.")
            print("Waiting 20 seconds before retrying...\n")

            time.sleep(20)

            continue

        except Exception:
            raise


def add_pseudocode_after_code(student, pseudocode):

    new_student = {}

    for key, value in student.items():

        new_student[key] = value

        if key == "Code":
            new_student["Pseudocode"] = pseudocode

    return new_student


def main():

    if not API_KEY:
        print("No API Key found. Please set the OPENAI_API_KEY environment variable before running.")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY)

    print("Validating API Key...")

    if not validate_api_key(client):
        print("Invalid API key. Please check OPENAI_API_KEY and run again.")
        sys.exit(1)

    print("API Key is valid. Starting processing...\n")

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:
        students = json.load(file)

    output = []

    total_students = len(students)

    for index, student in enumerate(students, start=1):

        user_id = student.get("User ID", "Unknown")

        print(
            f"Processing {index}/{total_students} "
            f"- User ID: {user_id}"
        )

        try:
            code = student.get("Code")

            if not code:
                raise Exception("Missing 'Code' field")

            pseudocode = call_api(client, code)

        except Exception as error:
            print(f"Error: {error}")

            pseudocode = f"ERROR: {error}"

        new_student = add_pseudocode_after_code(
            student,
            pseudocode
        )

        output.append(new_student)

        # Save the file every time after one student is done
        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                output,
                file,
                indent=2,
                ensure_ascii=False
            )

        # reduce rate limit
        if index < total_students:
            print("Waiting 15 seconds before next request...\n")
            time.sleep(15)

    print()
    print("Finished")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()