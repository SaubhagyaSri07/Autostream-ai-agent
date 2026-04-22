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
* LangGraph (Stateful Workflow Management)
* JSON (Knowledge Base)

---

## Project Structure

```
Autostream-agent/
│── main.py
│── langgraph_agent.py
│── intent.py
│── rag.py
│── llm.py
│── tools.py
│── knowledge_base.json
│── requirements.txt
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

This project uses LangGraph along with LangChain to implement a stateful, multi-step conversational agent. LangGraph was chosen because it allows modeling the conversation flow as a graph of nodes and transitions, making the system modular, scalable, and easier to manage compared to traditional if-else logic.

Each stage of the conversation is represented as a node in the graph, such as intent detection and lead capture. The system maintains a structured state object that stores key information like intent, current step, user details (name, email, platform), and response. This state is passed across nodes, enabling memory across multiple turns.

The workflow begins with the intent node, which classifies user input using the Gemini LLM. Based on the detected intent, the system either responds using RAG (for inquiries) or transitions to the lead capture node (for high-intent users). The lead capture node manages step-by-step data collection while handling interruptions and cancellations.

This architecture combines deterministic control flow with LLM reasoning, ensuring both reliability and flexibility. Compared to a manual state machine, LangGraph provides a cleaner abstraction for managing transitions and maintaining conversational state.

---

## WhatsApp Deployment (Using Webhooks)

To deploy this agent on WhatsApp, the system can be integrated using the WhatsApp Business API or services like Twilio.

The architecture would involve setting up a webhook endpoint using a framework like Flask or FastAPI. This webhook listens for incoming messages from WhatsApp. When a user sends a message, WhatsApp forwards it as an HTTP POST request to the webhook.

The server extracts the message content and passes it to the LangGraph agent. The agent processes the input using intent detection, RAG, or lead capture logic and generates a response. This response is then sent back to the user via the WhatsApp API.

### Steps:

1. Set up a webhook server (Flask or FastAPI)
2. Configure WhatsApp Business API or Twilio webhook URL
3. Forward incoming messages to the LangGraph agent
4. Send generated responses back using API calls

This setup enables real-time, scalable communication between users and the AI agent.

---

## Example Interaction

```
User: Hi  
Bot: Hello! How can I help you?  

User: What is pricing?  
Bot: Basic Plan: $29/month  
     Pro Plan: $79/month  

User: I want to buy  
Bot: What's your name?  

User: John  
Bot: Please provide your email.  
```

---

## Conclusion

This project demonstrates a real-world AI agent that combines:

* LLM-based reasoning
* Retrieval-Augmented Generation
* LangGraph-based state management
* Tool execution

It showcases how conversational AI systems can be designed to be both intelligent and reliable.
