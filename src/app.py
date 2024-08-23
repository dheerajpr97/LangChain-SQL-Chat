import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.utils.ui_components import configure_sidebar, configure_chat_interface, configure_db_connection, display_help
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from src.utils.langchain_utils import custom_prompt

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://archive.webdesignhot.com/wp-content/uploads/2013/04/Colorful-Abstract-Waves-on-Black-Background-Vector-Graphic_thumb.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>"""
st.markdown(background_image, unsafe_allow_html=True)

# Streamlit app configuration
#st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("LangChain: Chat with SQL DB")

# Sidebar Configuration
db_uri, mysql_host, mysql_user, mysql_password, mysql_db, api_key, uploaded_file = configure_sidebar()

if not api_key:
    st.info("Please add the Groq API key to proceed.")
else:
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-70b-8192", streaming=True)

    db = configure_db_connection(db_uri, mysql_host, mysql_user, mysql_password, mysql_db, uploaded_file)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Initialize memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create the agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        prompt_template=custom_prompt,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        max_iterations=15,
        max_execution_time=60,
        memory=memory
    )

    configure_chat_interface(agent)
    display_help()
