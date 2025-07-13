from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import AnyMessage
from langchain_ollama import OllamaLLM
from langchain_core.runnables import Runnable
from datetime import datetime

from graph.get_model import get_model

def chain(system_prompt: str, human_prompt: str, messages: list[AnyMessage], temperature: float, reasoning: bool) -> str:
    human_message: str = messages[-1].content # type: ignore

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(template=system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template(template=human_prompt, input_variables=["human_message", "timestamp"])
    ])

    model: OllamaLLM = get_model(temperature=temperature, reasoning=reasoning)

    chain: Runnable = prompt_template | model
    result: str = chain.invoke(input={"human_message": human_message, 
                                 "timestamp": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
                                 "messages": messages[:-1]})
    
    return result.split("Assistant: ")[-1]