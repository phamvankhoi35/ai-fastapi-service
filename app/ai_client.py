import os
from openai import OpenAI
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Khởi tạo client OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def ask_ai(messages) -> str:
    # Hàm gửi câu hỏi tới AI và nhận câu trả lời

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content