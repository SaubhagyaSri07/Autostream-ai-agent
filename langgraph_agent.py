from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from intent import detect_intent
from rag import get_answer
from tools import mock_lead_capture

import re


class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    step: Optional[str]
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    plan: Optional[str]
    response: Optional[str]


def is_question(text):
    text = text.lower()
    return "?" in text or any(w in text for w in ["what","how","why","price","plan","cost","feature","refund","support"])

def is_cancel(text):
    return any(w in text.lower() for w in ["cancel","stop","exit","leave","dont want","do not want","not interested"])

def is_valid_email(text):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', text) is not None

def is_valid_name(text):
    text_lower = text.lower()

    if any(word in text_lower for word in ["buy", "plan", "price"]):
        return False

    return all(p.isalpha() for p in text.split()) and len(text.strip()) > 1


def normalize_platform(text):
    text = text.lower()
    if "youtube" in text:
        return "YouTube"
    elif "insta" in text:
        return "Instagram"
    elif "twitter" in text or text == "x":
        return "Twitter/X"
    elif "tiktok" in text:
        return "TikTok"
    return text.capitalize()


def get_step_prompt(step):
    return {
        "name": "What's your name?",
        "email": "Please provide your email.",
        "platform": "Which platform do you create content on? (YouTube/Instagram/etc.)"
    }.get(step, "")


# =========================
# INTENT NODE
# =========================
def intent_node(state: AgentState):

    # Do not re-run intent if already in lead flow
    if state.get("intent") == "high_intent":
        return state

    user_input = state["user_input"]

    intent = detect_intent(user_input)

    # Force high intent if clear buying keywords
    if any(word in user_input.lower() for word in ["buy", "purchase", "subscribe"]):
        intent = "high_intent"

    # detect plan
    if "pro" in user_input.lower():
        state["plan"] = "Pro"
    elif "basic" in user_input.lower():
        state["plan"] = "Basic"

    state["intent"] = intent

    if intent == "greeting":
        state["response"] = "Hello! How can I help you?"

    elif intent == "inquiry":
        state["response"] = get_answer(user_input)

    elif intent == "high_intent":

        # RESET FLOW (important fix)
        state["step"] = "name"
        state["name"] = None
        state["email"] = None
        state["platform"] = None

        if state.get("plan"):
            state["response"] = f"Great choice! Let's get you started with the {state['plan']} plan.\n{get_step_prompt('name')}"
        else:
            state["response"] = get_step_prompt("name")

    else:
        state["response"] = "Sorry, I didn’t understand that."

    return state


# =========================
# LEAD NODE
# =========================
def lead_node(state: AgentState):

    user_input = state["user_input"]

    # cancel
    if is_cancel(user_input):
        state.update({
            "intent": None,
            "step": None,
            "name": None,
            "email": None,
            "platform": None,
            "response": "No problem! Let me know if you need anything else."
        })
        return state

    # interruption
    if is_question(user_input):
        state["response"] = get_answer(user_input) + "\n\n" + get_step_prompt(state["step"])
        return state

    # NAME
    if state["step"] == "name":

        if not is_valid_name(user_input):
            state["response"] = "Invalid name. Please enter your full name.\n" + get_step_prompt("name")
            return state

        state["name"] = user_input
        state["step"] = "email"
        state["response"] = "Got it. " + get_step_prompt("email")
        return state

    # EMAIL
    if state["step"] == "email":

        if not is_valid_email(user_input):
            if "gmal.com" in user_input or "gmial.com" in user_input:
                state["response"] = "Did you mean gmail.com? Please correct your email.\n" + get_step_prompt("email")
            else:
                state["response"] = "Invalid email format.\n" + get_step_prompt("email")
            return state

        state["email"] = user_input
        state["step"] = "platform"
        state["response"] = get_step_prompt("platform")
        return state

    # PLATFORM
    if state["step"] == "platform":

        if user_input.lower() in ["no","none","dont know","skip"]:
            state["response"] = "Please mention a platform like YouTube or Instagram.\n" + get_step_prompt("platform")
            return state

        state["platform"] = normalize_platform(user_input)

        mock_lead_capture(state["name"], state["email"], state["platform"])

        state.update({
            "intent": None,
            "step": None,
            "name": None,
            "email": None,
            "platform": None,
            "response": "Thank you! Our team will reach out to you soon."
        })

        return state

    return state


# =========================
# ROUTER
# =========================
def route_from_intent(state: AgentState):
    if state.get("intent") == "high_intent":
        return "lead"
    return END


# =========================
# GRAPH
# =========================
builder = StateGraph(AgentState)

builder.add_node("intent", intent_node)
builder.add_node("lead", lead_node)

builder.set_entry_point("intent")

builder.add_conditional_edges(
    "intent",
    route_from_intent,
    {
        "lead": "lead",
        END: END
    }
)

builder.add_edge("lead", END)

graph = builder.compile()