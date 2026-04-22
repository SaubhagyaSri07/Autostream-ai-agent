from intent import detect_intent
from rag import get_answer
from tools import mock_lead_capture
import re

# 🔹 Detect if input is a question
def is_question(text):
    text = text.lower()
    question_words = ["what", "how", "why", "price", "plan", "cost", "feature", "refund", "support"]
    return "?" in text or any(word in text for word in question_words)

# 🔹 Detect cancel intent
def is_cancel(text):
    text = text.lower()
    cancel_words = ["cancel", "stop", "exit", "leave", "dont want", "do not want", "not interested"]
    return any(word in text for word in cancel_words)

# 🔹 Validators
def is_valid_email(text):
    pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, text) is not None

def is_valid_name(text):
    return all(part.isalpha() for part in text.split()) and len(text.strip()) > 1

# 🔹 Normalize platform
def normalize_platform(text):
    text = text.lower()
    if "youtube" in text:
        return "YouTube"
    elif "insta" in text:
        return "Instagram"
    elif "twitter" in text or text == "x":
        return "Twitter/X"
    return text.capitalize()

# 🔹 Step prompts
def get_step_prompt(step):
    return {
        "name": "What's your name?",
        "email": "Please provide your email.",
        "platform": "Which platform do you create content on? (YouTube/Instagram/etc.)"
    }.get(step, "")

# 🔹 Reset state
def reset_state():
    return {
        "intent": None,
        "step": None,
        "name": None,
        "email": None,
        "platform": None,
        "plan": None  # ⭐ BONUS
    }

state = reset_state()

while True:
    user_input = input("You: ").strip()

    # ==============================
    # 🟢 LEAD CAPTURE MODE
    # ==============================
    if state["intent"] == "high_intent":

        if is_cancel(user_input):
            print("Bot: No problem! Let me know if you need anything else.")
            state = reset_state()
            continue

        if is_question(user_input):
            print("Bot:", get_answer(user_input))
            print("Bot:", get_step_prompt(state["step"]))
            continue

        intent_check = detect_intent(user_input).strip().lower()

        if intent_check in ["greeting", "high_intent"]:
            print("Bot:", get_step_prompt(state["step"]))
            continue

        # 🧩 NAME
        if state["step"] == "name":

            if not is_valid_name(user_input):
                print("Bot: Invalid name. Please enter your full name.")
                print("Bot:", get_step_prompt("name"))
                continue

            state["name"] = user_input
            state["step"] = "email"
            print("Bot: Got it 👍", get_step_prompt("email"))
            continue

        # 🧩 EMAIL
        elif state["step"] == "email":

            if not is_valid_email(user_input):
                if "gmal.com" in user_input or "gmial.com" in user_input:
                    print("Bot: Did you mean gmail.com? Please correct your email.")
                print("Bot: Invalid email format.")
                print("Bot:", get_step_prompt("email"))
                continue

            state["email"] = user_input
            state["step"] = "platform"
            print("Bot:", get_step_prompt("platform"))
            continue

        # 🧩 PLATFORM
        elif state["step"] == "platform":

            if user_input.lower() in ["no", "none", "dont know", "skip"]:
                print("Bot: Please mention a platform like YouTube or Instagram.")
                print("Bot:", get_step_prompt("platform"))
                continue

            state["platform"] = normalize_platform(user_input)

            mock_lead_capture(state["name"], state["email"], state["platform"])

            print("Bot: Thank you! Our team will reach out to you soon.")

            state = reset_state()
            continue

    # ==============================
    # 🟢 NORMAL MODE
    # ==============================
    intent = detect_intent(user_input).strip().lower()

    # ⭐ Detect plan (bonus)
    if "pro" in user_input.lower():
        state["plan"] = "Pro"
    elif "basic" in user_input.lower():
        state["plan"] = "Basic"

    if intent == "greeting":
        print("Bot: Hello! How can I help you?")

    elif intent == "inquiry":
        print("Bot:", get_answer(user_input))

    elif intent == "high_intent":
        state["intent"] = "high_intent"
        state["step"] = "name"

        if state["plan"]:
            print(f"Bot: Great choice! Let's get you started with the {state['plan']} plan.")
        print("Bot:", get_step_prompt("name"))

    else:
        print("Bot: Sorry, I didn’t understand that.")