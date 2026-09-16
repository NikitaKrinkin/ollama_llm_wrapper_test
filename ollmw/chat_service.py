from typing import List, Dict
from .llm_client import LlmClient, LLMClientError

class ChatService:
    def __init__(self, llm_client: LlmClient, default_system_prompt: str):
        self.client = llm_client
        self.default_system_prompt = default_system_prompt
        self.system_prompt: str | None = None
        self.history: List[Dict[str, str]] = []

    def is_prompt_set(self) -> bool:
        """
            Checks if the system prompt has been set for the current session.
        """
        return self.system_prompt is not None

    def set_system_prompt(self, prompt: str = "") -> str:
        """
            Sets the system prompt (from user input or defaults).
        """
        if not prompt.strip():
            self.system_prompt = self.default_system_prompt
            msg = f"Используется системный промпт по умолчанию: '{self.default_system_prompt}'"
        else:
            self.system_prompt = prompt.strip()
            msg = f"Установлен системный промпт: '{self.system_prompt}'"
        
        self.history.append({"role": "system_info", "content": msg})
        return msg

    def get_full_messages(self) -> List[Dict[str, str]]:
        """
            Builds the complete message payload to send to the LLM.
        """
        active_prompt = self.system_prompt if self.system_prompt else self.default_system_prompt
        messages = [{"role": "system", "content": active_prompt}]
        
        for msg in self.history:
            if msg["role"] in ["user", "assistant"]:
                messages.append(msg)
        return messages

    def send_message(self, user_message: str) -> str:
        text = user_message.strip()
        if not text:
            raise ValueError("Message cannot be empty.")

        self.history.append({"role": "user", "content": text})

        try:
            full_messages = self.get_full_messages()
            response_text = self.client.send_chat(full_messages)
            self.history.append({"role": "assistant", "content": response_text})
            return response_text
        except LLMClientError as e:
            self.history.pop()
            raise e

    def clear_history(self) -> None:
        """
            Clears chat history and resets the system prompt state.
        """
        self.history.clear()
        self.system_prompt = None

    def get_history(self) -> List[Dict[str, str]]:
        return list(self.history)
