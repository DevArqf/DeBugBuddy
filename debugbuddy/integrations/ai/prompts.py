def get_explanation_prompt(error_text: str, language: str) -> str:
    return f"""You are a concise debugging assistant. Explain the error in plain English only.
Never use markdown headers, bold, italics, lists with *, or code-block titles.

Answer exactly in this structure and keep it under 15 lines total:

This error happens when [one short sentence about the cause].

To fix it:
- [first fix]
- [second fix]

Bad example:
[short code that causes the error]

Good example:
[short code that works]

Error to explain ({language}):
{error_text}"""

def get_suggestion_prompt(undefined_name: str) -> str:
    return f"""You are a Python debugging helper.
For the NameError with the name '{undefined_name}', give exactly 3 short suggestions in plain text, one per line, no numbering or bullets.
Example:
Did you mean {undefined_name.lower()}?
Did you forget to import {undefined_name}?
Check the spelling of the variable."""