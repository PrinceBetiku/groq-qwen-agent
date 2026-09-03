import os
from dotenv import load_dotenv 
from langchain_core.messages import HumanMessage 
from langchain_groq import ChatGroq 
from langgraph.checkpoint.memory import MemorySaver 
from langgraph.prebuilt import create_react_agent 

# Load environment variables securely from local .env
load_dotenv()

def main():
    # Fix: Ensure you use a valid, active Qwen model string from Groq's documentation
    model = ChatGroq(
        model="qwen-2.5-72b", 
        temperature=0
    ) 

    # Empty list for now. You can easily plug custom tools here later!
    tools = []

    # In-memory checkpointer to persist thread history during this session
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "default_user_session"}}

    # Setting up the ReAct framework loop
    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    print("\n==============================================")
    print("🤖 LangGraph ReAct Agent Initialized via Groq")
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

        # Fix: Using stream_mode="messages" allows clean token-by-token terminal printing
        for msg, metadata in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        ):
            # Print content chunks from the model as they stream in
            if msg.content and metadata.get("langgraph_node") == "agent":
                print(msg.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()

