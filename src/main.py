import os
from dotenv import load_dotenv # Loads environment variables from .env file (secure API key handling)
from langchain_core.messages import HumanMessage # Standard message format for LangChain
from langchain_groq import ChatGroq # Groq API for fast LLM interface
from langgraph.checkpoint.memory import MemorySaver # Retains previous knowledge from prior chats in that session
from langchain.tools import tool # Placeholder for future tool definitions
from langgraph.prebuilt import create_react_agent # Pre-built ReAct agent framework

# Load environment variables (e.g., GROQ_API_KEY) before initializing the model.
# This keeps secrets out of version control and follows security best practices.

load_dotenv()

# Main execution loop for the AI Agent
# Initializes the model, creates a ReAct agent, and handles user interaction with streaming output.
def main():
    model = ChatGroq(model="qwen/qwen3.6-27b",temperature=0) # Initialize the LLM with Groq's Qwen model.
    # temperature=0 ensures repeatable responses

    tools = []

    memory = MemorySaver()

    config = {"configurable": {"thread_id": "default_user_session"}}

    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    print("Welcome, I am your personal AI Agent! Type quit to exit.")
    print("If you need to perform calculations or discuss things, I'll be right here.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            break

        if not user_input:
            continue

        print("\nAssistant: ", end="", flush=True)

        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="updates",
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk ["agent"]["messages"]:
                    if hasattr(message, "content") and message.content:
                        print(message.content, end="", flush=True)
        print()

if __name__ == "__main__":
    main()
