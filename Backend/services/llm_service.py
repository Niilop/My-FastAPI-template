from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from core.config import Settings, get_settings

settings = get_settings()

# Initialize the LLM
# We use the API key from your Pydantic settings
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.3,
    api_key=settings.api_key.get_secret_value() 
)

def summarize_text(text: str) -> str:
    """Uses LangChain to summarize the provided text."""
    
    # Create a simple prompt template
    prompt = PromptTemplate.from_template(
        "You are a helpful assistant. Please summarize the following text concisely:\n\n{text}"
    )
    
    # Build the LangChain pipeline (Prompt -> LLM)
    chain = prompt | llm
    
    # Execute the chain
    response = chain.invoke({"text": text})
    
    return response.content