import os
from dotenv import load_dotenv 
from langchain_core.messages import HumanMessage 
from langchain_groq import ChatGroq 
from langgraph.checkpoint.memory import MemorySaver 
from langgraph.prebuilt import create_react_agent 
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

# Load environment variables securely from a local .env file
load_dotenv()

# =====================================================================
# SKILL 1: Hand-Coded Mathematical Calculator
# =====================================================================
@tool
def calculate(expression: str) -> str:
    """Useful for evaluating math expressions. Input should be a valid mathematical expression string, such as '2 + 2' or '324.50 * 15'."""
    try:
        # Restrict access to dangerous underlying built-ins for base safety
        allowed_names = {"__builtins__": None}
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def main():
    # Initialize the high-intelligence Qwen model via Groq API
    model = ChatGroq(
        model="qwen-2.5-72b", 
        temperature=0
    ) 

    # SKILL 2: Dynamic Live Web Search Engine
    search_tool = DuckDuckGoSearchRun()

    # Register both active skills into your agent's routing array
    tools = [search_tool, calculate]

    # Persistent conversational memory for tracking thread histories
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "default_user_session"}}

    # Initialize the LangGraph ReAct state machine
    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    print("\n==============================================")
    print("🤖 LangGraph Multi-Tool Agent Initialized")
    print("Type 'quit' to exit the conversation.")
    print("==============================================\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("\nGoodbye! 👋")
            break

        if not user_input:
            continue

        print("\nAssistant: ", end="", flush=True)

        # Streams internal token segments directly to terminal print loops
        for msg, metadata in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        ):
            if msg.content and metadata.get("langgraph_node") == "agent":
                print(msg.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()
