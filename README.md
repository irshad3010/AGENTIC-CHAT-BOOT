# AGENTIC-CHAT-BOOT
E‑commerce Support Agent

You will build an AI‑powered customer support chatbot for a fictional e‑commerce application, using LangChain 1.x, Streamlit, and an SQLite database. The project must demonstrate:

A single conversational agent in LangChain 1.x that orchestrates all logic using tools.
A Streamlit UI for both customers and a simple admin view.
SQL‑backed queries and updates for orders, returns, tickets, and email logs.
A RAG component using ChromaDB for policy/FAQ questions.
Persistent conversation state using a LangChain checkpointer (not SQL).
Gmail notifications by passing the tools from the Gmail MCP Server to the agent.
Basic logging and observability via LangChain 1.x callbacks / middleware.
