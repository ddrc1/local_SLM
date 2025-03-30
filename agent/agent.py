import os
from typing import Dict, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from huggingface_hub import login
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
MODEL = os.getenv("MODEL")
LOCAL_DIR = "./models/checkpoints"

login(API_TOKEN)

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

llm = pipeline("text-generation", model=model, tokenizer=tokenizer, torch_dtype=torch.bfloat16, device_map="auto", max_new_tokens=4096)

def call(messages: List[BaseMessage], temperature=0.3) -> Dict["role", "content"]:
    role_conversion = {
        HumanMessage: "user",
        SystemMessage: "system",
        AIMessage: "assistant",
    }

    messages = [{"role": role_conversion[msg.__class__], "content": msg.content} for msg in messages]
    # llm_chain = LLMChain(llm=llm, prompt=PromptTemplate(template="{messages}", input_variables=["messages"]))
    # response = llm.invoke(messages, config={"temperature": temperature})
    # print(response)
    response = llm(messages, temperature=temperature)
    return response[0]['generated_text'][-1]