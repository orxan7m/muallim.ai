from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Разрешаем CORS-запросы с любых источников

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://orxan7m.github.io/muallim.ai/",
        "X-Title": "Muallim.AI"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты исламский советник. Отвечай строго по Корану, Сунне и мнениям достоверных учёных."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа.")
    except Exception as e:
        answer = "Ошибка при обращении к серверу."

    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Важно для Render
    app.run(host="0.0.0.0", port=port)
