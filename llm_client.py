# llm_client.py

from typing import Optional

try:
    # future: yaha real LLM client import karna
    # from langchain_openai import ChatOpenAI
    # from langchain_groq import ChatGroq
    LLM_AVAILABLE = False
except Exception:
    LLM_AVAILABLE = False


class DummyLLM:
    """
    Fallback LLM: jab real API nahi ho tab yeh simple rule-based text return karega.
    """
    def invoke(self, prompt: str) -> str:
        # Bahut simple behavior: prompt ke last lines ko hi return kar deta hai
        return "LLM placeholder response (no real model configured)."


def get_llm_client():
    """
    Future me yaha se real LLM connect hoga.
    Abhi ke liye DummyLLM return kar rahe hain, no API key needed.
    """
    if not LLM_AVAILABLE:
        return DummyLLM()

    # Example future code (jab tum OpenAI use karna chaho):
    # import os
    # from dotenv import load_dotenv
    # load_dotenv()
    # api_key = os.getenv("OPENAI_API_KEY")
    # return ChatOpenAI(model="gpt-4.1-mini", temperature=0.1, api_key=api_key)

    # For Groq in future:
    # return ChatGroq(model="llama-3.1-8b-instant", temperature=0.1, api_key=os.getenv("GROQ_API_KEY"))
