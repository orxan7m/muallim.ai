from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Muallim.AI backend работает!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    headers = {
        "Authorization": "Bearer sk-c4f10cf5f9254ecf871f4f55fe8a7733",  # ← твой ключ
        "Content-Type": "application/json",
        "HTTP-Referer": "https://orxan7m.github.io/muallim.ai",
        "X-Title": "Muallim.AI"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "Ты исламский советник. Отвечай строго по Корану, Сунне и мнениям достоверных учёных."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа.")
    except Exception as e:
        answer = f"Ошибка при запросе: {str(e)}"

    return jsonify({"answer": answer})


# 🔻 Обязательно добавь этот блок для Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render передаёт порт через переменную окружения
    app.run(host="0.0.0.0", port=port)
