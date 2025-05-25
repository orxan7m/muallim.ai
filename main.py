from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Разрешаем CORS
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    question = data.get("question")

    headers = {
        "Authorization": f"Bearer {openrouter_api_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://orxan7m.github.io/muallim.ai/",
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
        print("===> Ответ от OpenRouter:")
        print(result)  # 🔍 это важно для отладки

        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа.")
    except Exception as e:
        print("Ошибка:", e)
        answer = "Ошибка при запросе к OpenRouter."

    return jsonify({"answer": answer})


def openrouter_api_key():
    import os
    return os.environ.get("OPENROUTER_API_KEY", "ключ_не_задан")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
