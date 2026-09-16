import requests
from typing import List, Dict

class LLMClientError(Exception):
    pass

class LLMConnectionError(LLMClientError):
    pass

class LLMModelNotFoundError(LLMClientError):
    pass

class LlmClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def send_chat(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
        except requests.exceptions.ConnectionError:
            raise LLMConnectionError(
                "Не удалось подключиться к LLM. Убедитесь, что Ollama запущена."
            )
        except requests.exceptions.RequestException as e:
            raise LLMClientError(f"Network error: {e}")

        if response.status_code == 404:
            raise LLMModelNotFoundError(
                f"Не удалось получить ответ от модели. Проверьте, что модель {self.model} установлена."
            )
        elif response.status_code != 200:
            raise LLMClientError(
                f"API Ollama вернул ошибку ({response.status_code}): {response.text}"
            )

        data = response.json()
        return data.get("message", {}).get("content", "")
