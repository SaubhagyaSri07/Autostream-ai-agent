from llm import run_llm
from langchain_core.prompts import PromptTemplate
import json

def load_knowledge():
    with open("knowledge_base.json", "r") as f:
        return json.load(f)

knowledge = load_knowledge()

template = PromptTemplate.from_template("""
You are an AutoStream assistant.

Rules:
- Use ONLY the context
- If missing → say "I don't have that information."

Context:
{context}

Question: {question}
""")

def get_answer(query):
    context = f"""
Pricing:
{knowledge["pricing"]["basic"]}
{knowledge["pricing"]["pro"]}

Policies:
Refund: {knowledge["policies"]["refund"]}
Support: {knowledge["policies"]["support"]}
"""

    return run_llm(template.format(context=context, question=query)).strip()