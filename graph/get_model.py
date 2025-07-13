from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()

# __loaded_models: dict = {}

def get_model(model_name: str | None = None, temperature: float = 0, reasoning: bool = False) -> OllamaLLM:
    model_name = model_name or os.getenv("OLLAMA_MODEL", default="qwen3:1.7b")
    return OllamaLLM(model=model_name, temperature=temperature, reasoning=reasoning, num_gpu=1)

    