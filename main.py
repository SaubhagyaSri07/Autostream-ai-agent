from langgraph_agent import graph

state = {
    "intent": None,
    "step": None,
    "name": None,
    "email": None,
    "platform": None,
    "plan": None
}

while True:
    user_input = input("You: ").strip()

    state["user_input"] = user_input

    state = graph.invoke(state)

    print("Bot:", state["response"])