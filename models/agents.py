import io
import contextlib
import sqlite3
import pandas as pd
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_experimental.agents import create_pandas_dataframe_agent
from config import Config

class AgentManager:
    """Manages different types of agents"""
    
    def __init__(self):
        self.checkpointer = SqliteSaver(
            sqlite3.connect(Config.CHECKPOINT_DB, check_same_thread=False)
        )
    
    def create_react_agent(self, llm, tools):
        """
        Creates a ReAct agent with the given LLM and tools
        
        Args:
            llm: Language model instance
            tools: List of tools for the agent
            
        Returns:
            Agent executor
        """
        return create_react_agent(
            model=llm,
            tools=tools,
            prompt="You are a helpful assistant",
            checkpointer=self.checkpointer
        )
    
    def get_agent_response(self, agent, query: str, thread_id: str) -> str:
        """
        Gets response from agent for a given query
        
        Args:
            agent: The agent instance
            query: User query
            thread_id: Thread identifier for conversation
            
        Returns:
            Agent response as string
        """
        output = ''
        config = {"configurable": {"thread_id": thread_id}}

        input_message = {
            "role": "user",
            "content": query,
        }
        
        for step in agent.stream({"messages": [input_message]}, config, stream_mode="values"):
            last_msg = step["messages"][-1]

            # Capture pretty_print() output as string
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                last_msg.pretty_print()
                printed = buf.getvalue()

            output += "\n\n" + printed

        return output
    
    def create_dataframe_agent(self, llm, df: pd.DataFrame):
        """
        Creates a pandas DataFrame agent
        
        Args:
            llm: Language model instance
            df: Pandas DataFrame
            
        Returns:
            DataFrame agent
        """
        return create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            allow_dangerous_code=True,
            handle_parsing_errors=True
        )
    
    def query_dataframe(self, llm, df: pd.DataFrame, question: str) -> str:
        """
        Query a DataFrame using a pandas agent
        
        Args:
            llm: Language model instance
            df: Pandas DataFrame
            question: Question to ask about the data
            
        Returns:
            Answer as string
        """
        agent = self.create_dataframe_agent(llm, df)
        result = agent.invoke(question)
        return result['output']