from langchain_groq import ChatGroq
from app.config import settings

def get_llm(api_key: str = None):
    key = api_key or settings.GROQ_API_KEY

    if not key:
        return None

    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=key,
        temperature=0.1
    )
