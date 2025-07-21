import json
import re


def make_prompt(ocr_text, question):
    joined = "\n".join(ocr_text)
    return f"""
You are an AI resume coach.

Below is the extracted resume text:
--------------------
{joined}
--------------------

Now answer the following question based on the above text:
{question}
"""


def parse_response(raw_text, prompt):
    raw_text = raw_text[len(prompt) :]

    return {"response": raw_text.strip()}
