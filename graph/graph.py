from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import AnyMessage, HumanMessage
from graph.states.graph_state import GraphState
from graph.nodes.update_message import update_message
from graph.nodes.agent import agent


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
graph: StateGraph = StateGraph(GraphState)
graph.add_node(node="agent", action=agent)
# graph.add_node(answer_feedback)
graph.add_node(node="update_message", action=update_message)

graph.add_edge(START, "agent")
# graph.add_edge("call_model", "answer_feedback")
# graph.add_conditional_edges("answer_feedback", validate_answer, ['call_model', END])
graph.add_edge(start_key="agent", end_key="update_message")
graph.add_edge("update_message", END)

compiled_graph: CompiledStateGraph = graph.compile()

if __name__ == "__main__":

    while True:
        user_input = input("Write your question: ")

        response = compiled_graph.stream({"messages": [HumanMessage(user_input)]}, stream_mode="values")
        for event in response:
            # print(event)
            event["messages"][-1].pretty_print()