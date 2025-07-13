from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", default="qwen3:1.7b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", default="localhost")

# __loaded_models: dict = {}

def get_model(model_name: str | None = None, temperature: float = 0, reasoning: bool = False) -> OllamaLLM:
    model_name = model_name or OLLAMA_MODEL
    return OllamaLLM(
        model=model_name, 
        temperature=temperature, 
        reasoning=reasoning, 
        base_url=OLLAMA_HOST)

    