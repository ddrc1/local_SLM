from graph.states.graph_state import GraphState
from graph.chains.default_chain import chain
from graph.prompts.human_prompt import HUMAN_PROMPT
from graph.prompts.system_prompt import INITIAL_PROMPT

def agent(state: GraphState) -> GraphState:
    response: str = chain(
        messages=state['messages'],  # type: ignore
        temperature=state.get('temperature'), # type: ignore
        reasoning=state.get("reasoning"), # type: ignore
        human_prompt=HUMAN_PROMPT,
        system_prompt=INITIAL_PROMPT
    )
    print(response)
    return {"answer": response} # type: ignore