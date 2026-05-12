# init_db.py
import sqlite3

# Connect to the database file (it will be created if it doesn't exist)
connection = sqlite3.connect('database.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Define the SQL command to create the 'reviews' table
# This table will store an ID, a timestamp, the review text, the predicted sentiment, and the confidence score.
create_table_query = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    review_text TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    confidence REAL NOT NULL
);
"""

# Execute the command
cursor.execute(create_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database 'database.db' and table 'reviews' created successfully.")