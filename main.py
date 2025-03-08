from flask import Flask, request, jsonify
import os
from typing import Optional, Dict, List
from huggingface_hub import login
import torch
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_TOKEN = os.getenv("API_TOKEN")
MODEL = os.getenv("MODEL")
LOCAL_DIR = "./models/checkpoints"

login(API_TOKEN)

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, torch_dtype=torch.bfloat16, device_map="auto", max_new_tokens=4096)
llm = HuggingFacePipeline(pipeline=pipe)


def chat(messages: List[Dict["role", "content"]], temperature=0.3) -> Dict["generated_text", Dict["role", "content"]]:
    return pipe(messages, temperature=temperature)[0]

def validate_request(request: Dict) -> bool:
    request_data = request.json

    expected_fields = {"messages", "temperature"}
    extra_fields = set(request_data.keys()) - expected_fields
    if extra_fields:
        raise ValueError(f"Request contains unexpected fields: {', '.join(extra_fields)}")

    if "messages" not in request_data:
        raise ValueError("Request must contain 'messages' field")

    if not isinstance(request_data["messages"], list):
        raise ValueError("'messages' field must be a list")

    for message in request_data["messages"]:
        if "role" not in message:
            raise ValueError("Each message must contain 'role' field")
        if "content" not in message:
            raise ValueError("Each message must contain 'content' field")
        if not isinstance(message["role"], str):
            raise ValueError("'role' field must be a string")
        if not isinstance(message["content"], str):
            raise ValueError("'content' field must be a string")
    
    if "temperature" in request_data:
        if not isinstance(request_data["temperature"], (int, float)):
            raise ValueError("'temperature' field must be a number")
        if request_data["temperature"] < 0 or request_data["temperature"] > 1:
            raise ValueError("'temperature' field must be between 0 and 1")
    
    return request_data

@app.route("/chat", methods=["POST"])
def chat_response():
    try:
        request_data = validate_request(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return chat(**request_data)