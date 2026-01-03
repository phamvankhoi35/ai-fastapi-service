from rag import load_document, create_vector_db, search_docs
from ai_client import ask_ai

system_prompt = """
    Bạn là nhân viên CSKH.
    Chỉ trả lời dựa trên thông tin được cung cấp.
    Nếu không có thông tin, hãy nói bạn không chắc chắn.
"""

docs_text = load_document()
vector_db = create_vector_db(docs_text)

while True:
    user_input = input("Khach hang : ")
    if user_input.lower() in ["exit", "quit"]:
        break

    related_docs = search_docs(vector_db, user_input)
    context = "\n".join([doc.page_content for doc in related_docs])

    final_prompt = f"""
        Thông tin nội bộ:
        {context}

        Câu hỏi khách hàng:
        {user_input}
    """

    answer = ask_ai(system_prompt, final_prompt)
    print("AI: ", answer)

    """
        Thử hỏi:
            Shop giao hàng mấy ngày?
            Có hỗ trợ COD không?
            Có hoàn tiền sau 30 ngày không?
    """