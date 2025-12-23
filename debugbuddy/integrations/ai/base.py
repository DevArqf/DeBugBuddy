class BaseAIProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def explain_error(self, error_text, language):
        raise NotImplementedError