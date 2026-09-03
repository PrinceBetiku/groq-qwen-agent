import os
from html.parser import HTMLParser
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from dotenv import load_dotenv 
from langchain_core.messages import HumanMessage 
from langchain_groq import ChatGroq 
from langgraph.checkpoint.memory import MemorySaver 
from langgraph.prebuilt import create_react_agent 
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


class _SearchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._in_result = False
        self._text = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "result-link" in attributes.get("class", ""):
            self._in_result = True
            self._text = []

    def handle_data(self, data):
        if self._in_result:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._in_result:
            title = " ".join("".join(self._text).split())
            if title:
                self.results.append(title)
            self._in_result = False


@tool
def search_web(query: str) -> str:
    """Search the web and return the top result titles for a query."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=10) as response:
            parser = _SearchParser()
            parser.feed(response.read().decode("utf-8", errors="ignore"))
        return "\n".join(parser.results[:5]) or "No results found."
    except Exception as error:
        return f"Search failed: {error}"

def main():
    # Initialize the LLM with the verified Groq model ID
    model = ChatGroq(
        model="qwen/qwen3.6-27b", 
        temperature=0
    ) 

    tools = [search_web, calculate]

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
