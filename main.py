from fastapi import FastAPI
from pydantic import BaseModel
from ai_client import ask_ai
from rag import load_document, create_vector_db, search_docs

app = FastAPI()

system_prompt = """
    Bạn là chatbot CSKH.
    Chỉ trả lời dựa trên thông tin được cung cấp.
    Nếu không có thông tin, hãy nói bạn không chắc chắn.
"""

docs_text = load_document()
vector_db = create_vector_db(docs_text)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    related_docs = search_docs(vector_db, request.question)
    context = "\n".join(([doc.page_content for doc in related_docs]))

    final_prompt = f"""
        Thông tin nội bộ:
        {context}
    
        Câu hỏi khách hàng:
        {request.question}
    """

    answer = ask_ai(system_prompt, final_prompt)
    return {"answer": answer}

# gọi api thật, trả về api thật
# run terminal : uvicorn main:app --reload
# chrome : http://127.0.0.1:8000/docs
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