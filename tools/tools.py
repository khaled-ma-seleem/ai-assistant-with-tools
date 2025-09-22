import math
import requests
import numexpr
from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper 
from langchain_community.tools import WikipediaQueryRun
from services.vectorstore import VectorStoreManager

# Create a global vectorstore manager instance for the tools
_vectorstore_manager = VectorStoreManager()

@tool
def calculator_tool(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
    )

@tool
def weather_tool(location: str) -> str:
    """Get the current weather for a location.

    Example:
        "Cairo" or "New York"
    """
    try:
        response = requests.get(f"https://wttr.in/{location}?format=3")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Could not retrieve weather for {location}."
    except Exception as e:
        return f"Error retrieving weather: {e}"

@tool
def search_docs_tool(query: str) -> str:
    """
    Search relevant information from the document store.
    """
    return _vectorstore_manager.search_documents(query)

class ToolsManager:
    """Manages all available tools for agents"""
    
    def __init__(self):
        # Initialize Wikipedia API wrapper
        self.api_wrapper = WikipediaAPIWrapper(top_k_results=1) 
        self.wikipedia_tool = WikipediaQueryRun(api_wrapper=self.api_wrapper)
    
    def get_all_tools(self):
        """Returns list of all available tools"""
        return [
            calculator_tool,
            weather_tool,
            search_docs_tool,
            self.wikipedia_tool
        ]
