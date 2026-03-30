from typing import AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from core.config import Settings, get_settings

settings = get_settings()

_prompt = PromptTemplate.from_template(
    "You are a helpful assistant. Please summarize the following text concisely:\n\n{text}"
)

# Initialize the LLM
# We use the API key from your Pydantic settings
llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    temperature=0.3,
    api_key=settings.api_key.get_secret_value()
)

def summarize_text(text: str) -> str:
    """Uses LangChain to summarize the provided text."""
    chain = _prompt | llm
    response = chain.invoke({"text": text})
    return response.content

async def summarize_text_stream(text: str) -> AsyncGenerator[str, None]:
    """Async generator that streams summary tokens via LangChain's astream."""
    chain = _prompt | llm
    async for chunk in chain.astream({"text": text}):
        if chunk.content:
            yield chunk.content