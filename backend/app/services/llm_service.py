import os
from openai import OpenAI


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_answer(self, query: str, contexts: list[str]) -> str:
        context_text = "\n\n".join(contexts)

        prompt = f"""
Answer the question using the context below.
If the answer is not in the context, say "Not found in documents".

Context:
{context_text}

Question:
{query}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
