from fastapi import FastAPI
from pydantic import BaseModel

from ai_chatbot1.app.memory import get_history, add_message
from app.ai_client import ask_ai
from app.rag import load_documents, create_vector_db, search_docs

app = FastAPI()

system_prompt = """
    Bạn là chatbot CSKH.
    Chỉ trả lời dựa trên thông tin được cung cấp.
    Nếu không có thông tin, hãy nói bạn không chắc chắn.
"""

docs_text = load_documents()
vector_db = create_vector_db(docs_text)

class ChatRequest(BaseModel):
    session_id: str
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    history = get_history(request.session_id)

    related_docs = search_docs(vector_db, request.question)
    context = "\n".join([doc.page_content for doc in related_docs])

    messages = [
        {
            "role": "user",
            "content": "Bạn là chatbot CSKH"
        }
    ]

    messages += history
    messages.append({
        "role": "user",
        "content": request.question
    })

    final_prompt = f"""
        Thông tin nội bộ:
        {context}
    """

    answer = ask_ai(messages, final_prompt)

    add_message(request.session_id, "user", request.question)
    add_message(request.session_id, "assistant", answer)

    return {"answer": answer}

# gọi api thật, trả về api thật
# run terminal : uvicorn main:app --reload
# chrome :ttp://127.0.0.1:8000/docs
# {
#   "question": "Shop giao hàng mấy ngày?"
# }

"""
    AI = service
    Backend gọi AI
    Frontend chỉ gọi API
    
    build docker image, run : 
        docker build -t ai-chatbot .
    
    run container, run: 
        docker run -p 8000:8000 --env-file .env ai-chatbot

"""