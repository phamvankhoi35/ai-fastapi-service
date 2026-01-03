from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

def load_document():
    with open("documents.txt", "r", encoding="utf-8") as f:
        return f.read()

def create_vector_db(text: str):
    splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    docs = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_texts(docs, embeddings)
    return vector_db

def search_docs(vector_db, query: str):
    return vector_db.similarity_search(query, k=2)
