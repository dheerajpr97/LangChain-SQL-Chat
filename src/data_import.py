import sqlite3
import pandas as pd

# Load the preprocessed CSV
df = pd.read_csv('data/final_data.csv')

# Create a SQLite connection
conn = sqlite3.connect('db/ecommerce_data.db')

# Save the DataFrame to the SQLite database
df.to_sql('ecommerce', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Data successfully imported into SQLite database.")
