"""
check_openai_models.py
Run this to see which models are available on your API key.

Usage:
    export OPENAI_API_KEY=""
    python check_openai_models.py
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Fetch all available models
models = client.models.list()

# Filter to GPT models only and sort
gpt_models = sorted(
    [m.id for m in models.data if "gpt" in m.id.lower()],
    reverse=True
)

print("GPT models available on this key:")
print()
for m in gpt_models:
    print(f"  {m}")

print()
print("Recommended for your project:")
print("  - gpt-4o-mini  : fast, cheap, good enough for batch evaluation")
print("  - gpt-4o       : stronger reasoning, use for small comparison sample")
print("  - gpt-4o-mini  : best choice if quota is limited")