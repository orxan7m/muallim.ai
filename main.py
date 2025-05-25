from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    print("Вопрос от пользователя:", question)

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://orxan7m.github.io/muallim.ai",
        "X-Title": "Muallim.AI"
    }

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "system", "content": "Ты исламский советник. Отвечай строго по Корану и Сунне, ссылайся только на достоверные источники."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        print("Ответ от OpenRouter:", result)

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
        else:
            answer = "Ответ не получен от OpenRouter."

    except Exception as e:
        print("Ошибка при обращении к OpenRouter:", e)
        answer = "Ошибка при обращении к серверу."

    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
