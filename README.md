# LLM Chat Wrapper (Flask + Ollama)

Веб-приложение для взаимодействия с локальной моделью LLM через Ollama API.

## Требования
* Python 3.10+
* Установленный [Ollama](https://ollama.com/)

## Инструкция по запуску

1. **Запуск и настройка Ollama:**
```bash
ollama serve
ollama pull llama3.2:1b
```

2. **Подготовка окружения:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Запуск приложения:**
```bash
python main.py
```

Откройте `http://localhost:5000` в браузере.


