import random
from typing import Dict, List, Literal, Optional
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import SystemMessage, HumanMessage
from .agent import call

class CustomMessagesState(MessagesState):
    temperature: Optional[float] = 0.5

def call_model(message: CustomMessagesState) -> MessagesState:
    response = call(messages=message['messages'], temperature=message['temperature'])
    return {"messages": response}

# def answer_feedback(message: MessagesState) -> MessagesState:
#     validate_prompt = """Vou are a quality assurance bot.
#                          Given the user question, is the answer generated make sense or is valid? 
#                          Answer with 'yes' if is correct. 
#                          Otherwise, explain what is wrong to the other bot improve the answer."""
#     messages_to_validate = message['messages'][1:] + [SystemMessage(validate_prompt)]
#     response = call(messages_to_validate)
#     return {"messages": response}
    
# def validate_answer(message: MessagesState) -> Literal["call_model", END]:
#     feedback_message = message['messages'][-1]

#     if "yes" in feedback_message.content.lower():
#         print("Ending the process...")
#         return END
#     else:
#         print("Reruning the model call...")
#         return "call_model"
graph = StateGraph(CustomMessagesState)
graph.add_node(call_model)
# graph.add_node(answer_feedback)

graph.add_edge(START, "call_model")
# graph.add_edge("call_model", "answer_feedback")
# graph.add_conditional_edges("answer_feedback", validate_answer, ['call_model', END])
graph.add_edge("call_model", END)

graph = graph.compile()

def run_graph(messages: List[Dict["role", "content"]], temperature: float = 0.5):
    response = graph.invoke({"messages": messages, "temperature": temperature})
    return response

if __name__ == "__main__":
    while True:
        user_input = input("Write your question: ")

    # The config is the **second positional argument** to stream() or invoke()!
        response = graph.stream({"messages": [SystemMessage("You are a helpful chatbot. Think step by step."), 
                                            HumanMessage(user_input)]}, stream_mode="values")
        for event in response:
            # print(event)
            event["messages"][-1].pretty_print()