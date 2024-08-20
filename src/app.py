import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.ui_components import (
    configure_sidebar,
    configure_chat_interface,
    configure_db_connection,
    display_help,
    display_loading_indicator,
    export_query_results,
    handle_errors,
)
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from src.db_utils import configure_db
from src.langchain_utils import custom_prompt
import groq

# Streamlit app configuration
st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("LangChain: Chat with SQL DB")

# Sidebar Configuration
db_uri, mysql_host, mysql_user, mysql_password, mysql_db, api_key = configure_sidebar()

if not api_key:
    st.info("Please add the Groq API key to proceed.")
else:
    # LLM model
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

    # Configure the database connection
    db = configure_db_connection(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)

    # Toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # SQL Agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        prompt_template=custom_prompt,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        max_iterations=10,  # Increase the iteration limit
        max_execution_time=60  # Increase the time limit (in seconds)
    )

    # Chat Interface
    configure_chat_interface(agent)

    # Display Help Section
    display_help()

