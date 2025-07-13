from langchain_core.messages import AIMessage

from graph.states.graph_state import GraphState


def update_message(state: GraphState) -> GraphState:
    answer: str = state['answer'] # type: ignore
    return {'messages': AIMessage(answer)} # type: ignore