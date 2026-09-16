from flask import Flask, render_template, request, jsonify
from .config import Config
from .llm_client import LlmClient, LLMClientError
from .chat_service import ChatService

app = Flask(__name__)
app.config.from_object(Config)

client = LlmClient(base_url=app.config["LLM_BASE_URL"], model=app.config["LLM_MODEL"])
chat_service = ChatService(llm_client=client, default_system_prompt=app.config["SYSTEM_PROMPT"])

@app.route("/")
def index():
    return render_template(
        "index.html", 
        history=chat_service.get_history(),
        prompt_set=chat_service.is_prompt_set()
    )

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    is_system_init = data.get("is_system_init", False)
    use_default = data.get("use_default", False)

    try:
        # Prompt initialization
        if is_system_init:
            if use_default:
                msg = chat_service.set_system_prompt("")
            else:
                if not user_message.strip():
                    return jsonify({"error": "Системный промпт не может быть пустым."}), 400
                msg = chat_service.set_system_prompt(user_message)
            return jsonify({"response": msg, "type": "system_info"})

        # Regular chatting
        if not user_message.strip():
            return jsonify({"error": "Пустое сообщение отправлять нельзя."}), 400

        reply = chat_service.send_message(user_message)
        return jsonify({"response": reply, "type": "assistant"})

    except LLMClientError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Внутренняя ошибка сервера: {str(e)}"}), 500

@app.route("/api/clear", methods=["POST"])
def clear():
    chat_service.clear_history()
    return jsonify({"status": "ok"})

