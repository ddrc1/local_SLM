from langgraph.graph import MessagesState


class GraphState(MessagesState):
    temperature: float | None
    reasoning: bool | None
    answer: str | None