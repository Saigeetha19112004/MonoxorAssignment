# stock_multi_agent/multiagent.py

from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.core import Session, runner
from dotenv import load_dotenv
import os

# Load environment variables from the .env file in the current directory
env_path = '.env'
if os.path.exists(env_path):
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            pass  # Just to check encoding
        load_dotenv(env_path)
    except UnicodeDecodeError:
        print("Error: .env file is not valid UTF-8. Please re-save it as UTF-8 without BOM.")
else:
    print("Warning: .env file not found.")

# Import your agent functions from the 'agents' package
from agents.identify_ticker import get_ticker_from_query
from agents.ticker_price import get_current_stock_price
from agents.ticker_news import get_latest_news
from agents.ticker_price_change import get_price_change
from agents.ticker_analysis import analyze_stock

# Define your individual agents (these are defined once globally)
identify_ticker = Agent(
    name="identify_ticker",
    description="Extracts stock ticker",
    tools=[get_ticker_from_query]
)
ticker_price = Agent(
    name="ticker_price",
    description="Fetches current price",
    tools=[get_current_stock_price]
)
ticker_news = Agent(
    name="ticker_news",
    description="Gets latest news",
    tools=[get_latest_news]
)
ticker_price_change = Agent(
    name="ticker_price_change",
    description="Calculates price change",
    tools=[get_price_change]
)
ticker_analysis = Agent(
    name="ticker_analysis",
    description="Analyzes price and news",
    tools=[analyze_stock]
)

# Instead of subagents, combine all functions as tools for the orchestrator
orchestrator = Agent(
    name="stock_orchestrator",
    description="Answers stock-related queries by routing to appropriate agent",
    tools=[
        get_ticker_from_query,
        get_current_stock_price,
        get_latest_news,
        get_price_change,
        analyze_stock
    ]
)


try:
    from google.adk.core import Session, runner
except ImportError:
    # If this fails, check your google.adk version and documentation for correct import paths
    print("Error: Could not import Session and runner from google.adk.core. Please check your google.adk installation.")
    # Optionally, you can raise or exit here

# This function encapsulates the multi-agent system's core logic
def run_stock_query(query: str) -> str:
    """
    Runs a stock-related query through the multi-agent system.
    """
    memory_service = InMemoryMemoryService()
    session = Session(memory=memory_service)
    try:
        response = runner.run(orchestrator, session=session, input=query)
        return response
    except Exception as e:
        # Basic error handling for the web interface
        return f"An error occurred during agent execution: {e}"

# This block allows multiagent.py to still be run directly from the command line for testing
if __name__ == "__main__":
    test_query = "Why did Tesla stock fall today?"
    print(f"Running test query via command line: '{test_query}'")
    result = run_stock_query(test_query)
    print(result)