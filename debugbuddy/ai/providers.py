import os
from debugbuddy.ai.prompts import get_explanation_prompt
from typing import Optional, Dict, Any

class OpenAIProvider:
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.api_key = api_key
        self.model = config.get('ai_model', 'gpt-3.5-turbo')
        self.client = None
        if api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
            except ImportError:
                pass

    def explain_error(self, error_text: str, language: str) -> Optional[str]:
        if not self.client:
            return "OpenAI not available"

        prompt = get_explanation_prompt(error_text, language)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI error: {str(e)}"


class AnthropicProvider:
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.api_key = api_key
        self.model = config.get('ai_model', 'claude-3-5-sonnet-20241022')
        self.client = None
        if api_key:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key)
            except ImportError:
                pass

    def explain_error(self, error_text: str, language: str) -> Optional[str]:
        if not self.client:
            return "Anthropic not available"

        prompt = get_explanation_prompt(error_text, language)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.2,
                system="You are a concise debugging assistant. Follow the exact format requested.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"Anthropic error: {str(e)}"


def get_provider(provider_name: str, config: Dict[str, Any]) -> Optional[Any]:
    if provider_name == "openai":
        return OpenAIProvider(config.get("openai_api_key"), config)
    elif provider_name == "anthropic":
        return AnthropicProvider(config.get("anthropic_api_key"), config)
    return None