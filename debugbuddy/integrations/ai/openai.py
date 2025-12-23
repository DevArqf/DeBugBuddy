from openai import OpenAI
from .base import BaseAIProvider
from .prompts import ERROR_EXPLANATION_PROMPT

class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key, model='gpt-4'):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def explain_error(self, error_text, language):
        prompt = ERROR_EXPLANATION_PROMPT.format(error=error_text, language=language)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content