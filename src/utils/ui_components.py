import streamlit as st
import groq
import pandas as pd
from io import BytesIO
from src.utils.db_utils import configure_db


def configure_sidebar():
    """
    Configures the sidebar for the Streamlit app, including database connection details
    and the Groq API key input.
    """
    radio_opt = ["Use SQLite 3 Database - ecommerce_data.db", "Connect to your MySQL Database"]
    selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat with:", options=radio_opt)

    mysql_host = mysql_user = mysql_password = mysql_db = None

    if radio_opt.index(selected_opt) == 1:
        db_uri = "USE_MYSQL"
        mysql_host = st.sidebar.text_input("Provide MySQL Host")
        mysql_user = st.sidebar.text_input("MySQL User")
        mysql_password = st.sidebar.text_input("MySQL Password", type="password")
        mysql_db = st.sidebar.text_input("MySQL Database")
    else:
        db_uri = "USE_LOCALDB"

    api_key = st.sidebar.text_input(label="Groq API Key", type="password")

    st.sidebar.markdown("---")
    export_query_results()  # Place the export button in the sidebar

    return db_uri, mysql_host, mysql_user, mysql_password, mysql_db, api_key


def configure_chat_interface(agent):
    """
    Configures the chat interface for the Streamlit app, managing session state and handling user input.
    """
    if st.button("Clear message history"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    elif "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    MAX_MESSAGES = 5

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query = st.chat_input(placeholder="Ask anything from the database")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        messages_to_send = st.session_state.messages[-MAX_MESSAGES:]

        with st.chat_message("assistant"):
            try:
                display_loading_indicator()  # Show a loading spinner
                response = agent.run({"input": user_query, "history": messages_to_send})
            except ValueError as e:
                handle_errors(e)
            except groq.APIStatusError as e:
                handle_errors(e)
            else:
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

def configure_db_connection(db_uri, mysql_host, mysql_user, mysql_password, mysql_db):
    """
    Configures the database connection based on the selected database type.
    """
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
    return db


def display_help():
    """
    Displays a help section in the sidebar or as a collapsible element to assist users.
    """
    with st.sidebar.expander("Help", expanded=False):
        st.write("""
            - **Database Options**: Choose the appropriate database type.
            - **API Key**: Ensure you provide the correct Groq API key to interact with the LLM.
            - **User Queries**: Type your queries in the chat input box.
        """)


def display_loading_indicator():
    """
    Displays a loading spinner to indicate that the app is processing a query.
    """
    with st.spinner("Processing..."):
        pass

def handle_errors(exception):
    """
    Handles and displays errors during the execution of the app.
    """
    st.error(f"An error occurred: {str(exception)}")

def export_query_results():
    """
    Adds an export button to the sidebar to allow users to download query results as a CSV file.
    It collects all 'assistant' responses that are assumed to be results from the SQL queries.
    """

    # Initialize messages key if not exists
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        
    results = [msg["content"] for msg in st.session_state["messages"] if msg["role"] == "assistant"]

    if results:
        try:
            df = pd.DataFrame([result.split(',') for result in results])
            csv = df.to_csv(index=False)
            b = BytesIO()
            b.write(csv.encode('utf-8'))
            b.seek(0)

            st.sidebar.download_button(
                label="Export Results as CSV",
                data=b,
                file_name="query_results.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.sidebar.error(f"Error exporting results: {str(e)}")
    else:
        st.sidebar.warning("No results to export.")