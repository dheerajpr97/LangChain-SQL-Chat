import sqlite3
from pathlib import Path
import streamlit as st
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# @st.cache_resource(ttl="2h")
# def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
#     """
#     Configures a database connection based on the provided URI.

#     Parameters:
#     db_uri (str): The URI of the database to connect to. Can be either LOCALDB or MYSQL.
#     mysql_host (str): The host of the MySQL database. Required if db_uri is MYSQL.
#     mysql_user (str): The username to use for the MySQL database connection. Required if db_uri is MYSQL.
#     mysql_password (str): The password to use for the MySQL database connection. Required if db_uri is MYSQL.
#     mysql_db (str): The name of the MySQL database to connect to. Required if db_uri is MYSQL.

#     Returns:
#     SQLDatabase: A configured SQLDatabase object.
#     """
#     if db_uri == LOCALDB:
#         # Ensure the database file path is correct
#         dbfilepath = Path(__file__).parent / "../../db/ecommerce_data.db"
#         if not dbfilepath.exists():
#             st.error(f"SQLite database file not found at {dbfilepath}")
#             st.stop()
#         creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
#         return SQLDatabase(create_engine("sqlite:///", creator=creator, connect_args={"check_same_thread": False}))
#     elif db_uri == MYSQL:
#         if not (mysql_host and mysql_user and mysql_password and mysql_db):
#             st.error("Please provide all MySQL connection details.")
#             st.stop()
#         return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

# @st.cache_resource(ttl="2h")
# def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None, uploaded_file=None):
#     if db_uri == LOCALDB:
#         dbfilepath = Path(__file__).parent / "../../db/ecommerce_data.db"
#         if not dbfilepath.exists():
#             st.error(f"SQLite database file not found at {dbfilepath}")
#             st.stop()
#         creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
#         return SQLDatabase(create_engine("sqlite:///", creator=creator, connect_args={"check_same_thread": False}))
#     elif db_uri == MYSQL:
#         if not (mysql_host and mysql_user and mysql_password and mysql_db):
#             st.error("Please provide all MySQL connection details.")
#             st.stop()
#         return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
#     elif db_uri == "CUSTOMDB" and uploaded_file is not None:
#         with open("uploaded_database.db", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         creator = lambda: sqlite3.connect(f"file:uploaded_database.db?mode=ro", uri=True)
#         return SQLDatabase(create_engine("sqlite:///", creator=creator, connect_args={"check_same_thread": False}))
#     else:
#         st.error("Invalid database configuration.")
#         st.stop()

import pandas as pd
import sqlite3

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None, uploaded_file=None):
    if db_uri == LOCALDB:
        dbfilepath = Path(__file__).parent / "../../db/ecommerce_data.db"
        if not dbfilepath.exists():
            st.error(f"SQLite database file not found at {dbfilepath}")
            st.stop()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator, connect_args={"check_same_thread": False}))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    elif db_uri == "CUSTOMDB" and uploaded_file is not None:
        with open("uploaded_database.db", "wb") as f:
            f.write(uploaded_file.getbuffer())
        creator = lambda: sqlite3.connect(f"file:uploaded_database.db?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator, connect_args={"check_same_thread": False}))
    elif db_uri == "CSVDB" and uploaded_file is not None:
        # Create a temporary SQLite database from the uploaded CSV
        temp_db_path = "temporary_database.db"
        conn = sqlite3.connect(temp_db_path)
        try:
            df = pd.read_csv(uploaded_file)
            df.to_sql("uploaded_data", conn, index=False, if_exists="replace")
        except Exception as e:
            st.error(f"Error processing CSV file: {e}")
            st.stop()
        creator = lambda: sqlite3.connect(f"file:{temp_db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator, connect_args={"check_same_thread": False}))
    else:
        st.error("Invalid database configuration.")
        st.stop()
