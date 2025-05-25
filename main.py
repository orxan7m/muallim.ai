from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"answer": "Вопрос не получен."})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Ты исламский ассистент. Отвечай строго по Корану, Сунне и мнениям достоверных учёных."},
                {"role": "user", "content": question}
            ]
        }

        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        result = response.json()

        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа.")
        return jsonify({"answer": answer})

    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"answer": "Ошибка при обращении к серверу."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
