from llm import run_llm
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("""
You are a strict intent classifier.

Classify into EXACTLY one:
- greeting
- inquiry
- high_intent

Rules:
- Questions → inquiry
- Buying intent → high_intent
- Greetings → greeting
- Names/emails/random → unknown

Input: {input}

Return ONLY one word.
""")

def detect_intent(user_input):
    result = run_llm(template.format(input=user_input))
    cleaned = result.lower().strip().replace(".", "").replace("\n", "")

    if cleaned not in ["greeting", "inquiry", "high_intent"]:
        return "unknown"

    return cleaned