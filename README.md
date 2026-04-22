# AutoStream AI Sales Agent

## Overview

AutoStream AI Sales Agent is an intelligent conversational agent designed to simulate a real-world sales assistant. It uses LLM-based reasoning along with structured workflows to handle user queries and capture leads efficiently.

The system supports multi-turn conversations, interruption handling, and dynamic state transitions, making it suitable for real-world deployment scenarios.

---

## Features

### Intent Detection

* Classifies user input into:

  * Greeting
  * Inquiry
  * High Intent (purchase-ready users)
* Implemented using Gemini LLM with prompt engineering

---

### RAG-based Knowledge Retrieval

* Uses a local knowledge base (`knowledge_base.json`)
* Provides grounded responses for:

  * Pricing
  * Refund policy
  * Support

---

### Lead Capture System

* Triggered only when high intent is detected
* Collects:

  * Name
  * Email
  * Platform
* Executes tool only after all data is collected

---

### Conversation Handling

* Interruptible flow (answers questions mid-process)
* Resumes previous step after interruption
* Allows cancellation at any time
* Input validation and normalization

---

## Tech Stack

* Python
* Gemini API (LLM)
* LangChain (Prompt Templates)
* JSON (Knowledge Base)

---

## Project Structure

```
Autostream-agent/
│── main.py
│── intent.py
│── rag.py
│── llm.py
│── tools.py
│── knowledge_base.json
│── .env
```

---

## How to Run the Project Locally

1. Clone the repository:

```
git clone <your-repo-link>
cd Autostream-agent
```

2. Create a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Add your Gemini API key in `.env`:

```
GEMINI_API_KEY=your_api_key_here
```

5. Run the application:

```
python main.py
```

---

## Architecture Explanation

This project uses LangChain as the framework for integrating LLM-based reasoning with structured workflows. LangChain was chosen because it provides a simple and modular way to design prompt-driven applications while maintaining flexibility in how LLM calls are managed. Instead of using a fully automated agent framework like AutoGen, this implementation uses a controlled state machine approach to ensure predictable and stable behavior.

State management is handled using a dictionary-based state object that tracks the current intent and step in the conversation (e.g., name, email, platform). This allows the system to maintain context across multiple turns and resume the correct step after interruptions. The flow is divided into two modes: normal conversation mode and lead capture mode. In normal mode, the system uses intent detection to decide whether to respond using RAG or transition into lead capture. In lead capture mode, inputs are validated and processed sequentially, while still allowing interruptions such as user queries or cancellation.

This hybrid design combines deterministic control flow with LLM-based reasoning, ensuring both reliability and flexibility in handling real-world conversations.

---

## WhatsApp Deployment (Using Webhooks)

To deploy this agent on WhatsApp, the system can be integrated using the WhatsApp Business API or services like Twilio.

The architecture would involve setting up a webhook endpoint (e.g., using Flask or FastAPI) that listens for incoming messages from WhatsApp. When a user sends a message, WhatsApp forwards it to the webhook as an HTTP POST request. The server extracts the message content and passes it to the chatbot logic (main.py).

The chatbot processes the input using intent detection, RAG, or lead capture logic and generates a response. This response is then sent back to the user via the WhatsApp API.

Key steps:

1. Set up a webhook server (Flask/FastAPI)
2. Configure WhatsApp Business API or Twilio webhook URL
3. Forward incoming messages to chatbot logic
4. Send responses back using API calls

This setup allows real-time, scalable communication between users and the AI agent.

---

## Example Interaction

```
User: Hi  
Bot: Hello! How can I help you?  

User: What is pricing?  
Bot: [Displays pricing]  

User: I want to buy  
Bot: What's your name?  
```

---

## Conclusion

This project demonstrates a real-world AI agent that combines:

* LLM-based reasoning
* Retrieval-Augmented Generation
* Structured state management
* Tool execution

It showcases how conversational AI systems can be designed to be both intelligent and reliable.
