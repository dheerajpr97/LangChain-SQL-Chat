import sqlite3
from pathlib import Path

import streamlit as st
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    """
    Configures a database connection based on the provided URI.

    Parameters:
    db_uri (str): The URI of the database to connect to. Can be either LOCALDB or MYSQL.
    mysql_host (str): The host of the MySQL database. Required if db_uri is MYSQL.
    mysql_user (str): The username to use for the MySQL database connection. Required if db_uri is MYSQL.
    mysql_password (str): The password to use for the MySQL database connection. Required if db_uri is MYSQL.
    mysql_db (str): The name of the MySQL database to connect to. Required if db_uri is MYSQL.

    Returns:
    SQLDatabase: A configured SQLDatabase object.
    """
    if db_uri == LOCALDB:
        # Ensure the database file path is correct
        dbfilepath = Path(__file__).parent / "../db/ecommerce_data.db"
        if not dbfilepath.exists():
            st.error(f"SQLite database file not found at {dbfilepath}")
            st.stop()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))