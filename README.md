# LangChain: Chat with SQL Database

## Overview

**LangChain: Chat with SQL Database** is an interactive application that allows users to interact with SQL databases using natural language queries. The system leverages LangChain to translate user queries into SQL commands and execute them against a connected database. It supports SQLite, MySQL databases, custom SQL databases, and even temporary databases created from uploaded CSV files, providing users with flexibility in database management.

The app includes features such as conversational querying, message history management, database uploads, and result exporting, all within an intuitive, interactive UI powered by Streamlit. The latest version also introduces enhanced error handling, session management, and the ability to switch between different databases seamlessly, including the option to upload custom databases or CSV files.

## Functionalities

Upon launching the Streamlit app, users are presented with the following functionalities:

1. **Natural Language SQL Querying**:
   - Translate natural language queries into SQL and execute them against the connected database.
   - Supports SQLite (default `ecommerce_data.db`), MySQL databases, custom SQLite databases, and temporary databases created from uploaded CSV files.

2. **Session Management**:
   - Maintain and clear message history across sessions, ensuring context-aware interactions.
   - Export query results to a CSV file directly from the sidebar for further analysis.

3. **Database Flexibility**:
   - Choose between a local SQLite database, a custom SQL database, a MySQL database, or create a temporary database from an uploaded CSV file.

## Features

- **Custom Database Upload**: Upload your own SQL database file to interact with custom datasets on the fly.
- **CSV to Database**: Upload a CSV file, which will be converted into a temporary SQL database for interaction.
- **Conversational Querying**: Interact with your database through a chat interface that translates natural language into SQL queries.
- **Message History**: Maintain context across queries, allowing for more coherent and contextually aware conversations.
- **Result Export**: Easily export the results of your queries as a CSV file.
- **Interactive UI**: A user-friendly interface built with Streamlit for seamless interaction with your SQL databases.
- **Clear History**: Reset the conversation history at any time using the sidebar control.

## Setup

### Prerequisites

- Python 3.8 or higher
- Install the required dependencies listed in `requirements.txt`

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/dheerajpr97/LangChain-SQL-Chat.git
   cd LangChain-SQL-Chat
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add the necessary API keys.
   ```bash
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Set Up the Database**

   The application can interact with SQL databases (including custom ones), MySQL databases, or a temporary database created from a CSV file.

   - **Default SQLite Database**: To set up the default SQLite database:

     - **Run the Data Import Script**: This will create and populate the `ecommerce_data.db` SQLite database with sample data.

       ```bash
       python src/data_import.py
       ```

     The database file `ecommerce_data.db` will be created in your project's root directory.

   - **Custom SQLite Database**: If you have your own SQL database with a `.db` extension, you can upload it directly through the application's UI.

   - **CSV File**: If you have a CSV file, you can upload it, and the app will create a temporary SQL database from it.

   - **MySQL Setup (Optional)**: If you prefer to use a MySQL database, ensure your MySQL server is running, and you have created a database. You will need to provide the MySQL connection details in the app's sidebar when you start the application.

### Running the Application

To start the Streamlit app from the 'src' directory:

```bash
streamlit run app.py
```

This will launch the app in your default web browser. You can now interact with your database using natural language queries.

## Usage

- **Selecting a Database**: Choose between the local SQLite database (`ecommerce_data.db`), a custom SQLite database, a MySQL database, or upload a CSV file to create a temporary SQLite database.
- **Entering Groq API Key**: Input your Groq API key in the sidebar to enable LLM-powered query translation.
- **Running Queries**: Type your query into the chat input field. The application will translate it into SQL, execute it, and return the results.
- **Exporting Results**: Use the "Export Results as CSV" button in the sidebar to download the results of your queries.
- **Clearing Chat History**: Click the "Clear message history" button in the sidebar to reset your chat session.

## Watch the Demo

[SQLite Demonstration Video](https://github.com/user-attachments/assets/d602849c-c330-4a1f-8de3-4efc0b0668bf)

The first video demonstrates how to use the E-Commerce data from [Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data) with SQLite. 

[MySQL Demonstration Video](https://github.com/user-attachments/assets/cf9232c2-e4a3-4190-a230-3a3650d80fb0)

The second video focuses on utilizing the example SAKILA database within a MySQL environment.

## Future Developments

- **Enhanced Query Parsing**: Improve the natural language understanding for more complex SQL queries.
- **Cloud Deployment**: Deploy the application on cloud platforms like AWS or GCP for better scalability and accessibility.
- **Additional Database Support**: Extend support to other types of databases, such as PostgreSQL or MongoDB.
- **Real-Time Query Optimization**: Implement real-time feedback and optimization techniques to improve query performance based on user interactions.

## Acknowledgements

We would like to extend our gratitude to the following organizations and tools that made this project possible:

- **[GROQ](https://groq.com/)**: For providing the advanced LLM (Llama-3) used in this project.
- **[LangChain](https://langchain.com/)**: For offering a robust framework to build and integrate language model applications.
- **[Streamlit](https://streamlit.io/)**: For enabling the creation of an intuitive and interactive user interface.
- **[SQLite](https://www.sqlite.org/)** and **[MySQL](https://www.mysql.com/)**: For the robust database management systems used in this project.

We appreciate the open-source community and the developers who contribute to these projects, making tools and resources freely available for everyone to use and build upon.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.