from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # <-- это разрешает доступ с любых доменов

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа.")
    except Exception as e:
        print(e)
        answer = "Ошибка при запросе к OpenRouter."

    return jsonify({"answer": answer})
