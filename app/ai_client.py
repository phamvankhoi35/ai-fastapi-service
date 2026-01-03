import os
from openai import OpenAI
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Khởi tạo client OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def ask_ai(system_prompt: str, user_prompt: str) -> str:
    # Hàm gửi câu hỏi tới AI và nhận câu trả lời
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3
    )
    return res.choices[0].message.content