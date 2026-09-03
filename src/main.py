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

@tool
def calculate(expression: str) -> str:
    """Useful for evaluating math expressions. Input should be a valid mathematical expression string, such as '2 + 2' or '324.50 * 15'."""
    try:
        allowed_names = {"__builtins__": None}
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def main():
    # Initialize the LLM with the verified Groq model ID
    model = ChatGroq(
        model="qwen/qwen3.6-27b", 
        temperature=0
    ) 

    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool, calculate]

    # Persistent conversational memory checkpointer
    memory = MemorySaver()
    
    # Unique thread configuration allows the checkpointer to map conversation history
    config = {"configurable": {"thread_id": "default_user_session"}}

    # Setting up the LangGraph ReAct state machine
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

        # Correct Tuple Unpacking: extract the inner message object and the node metadata
        for message, metadata in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        ):
            # Only print text chunks originating from the agent node to keep the console clean
            if metadata.get("langgraph_node") == "agent" and message.content:
                print(message.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()
