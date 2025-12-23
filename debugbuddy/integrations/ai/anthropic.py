from anthropic import Anthropic
from .base import BaseAIProvider
from .prompts import ERROR_EXPLANATION_PROMPT

class AnthropicProvider(BaseAIProvider):
    def __init__(self, api_key, model='claude-3-opus-20240229'):
        super().__init__(api_key)
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def explain_error(self, error_text, language):
        prompt = ERROR_EXPLANATION_PROMPT.format(error=error_text, language=language)
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text