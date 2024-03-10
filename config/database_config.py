import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('../du.db')

# Create a cursor object
cursor = connection.cursor()

# Create the characters table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        username TEXT,
        email TEXT,
        password TEXT
    )
""")

# Define your characters data
characters_list = [
	("Barron", "jo...@gmail.com", "...."),
	("Valdoom", "j...@gmail.com", "...")
]

# Insert data into the characters table
cursor.executemany("""
    INSERT INTO characters (username, email, password)
    VALUES (?, ?, ?)
""", characters_list)

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

import sqlite3


class DatabaseManager:
	def __init__(self, db_name):
		self.db_name = db_name
		self.connection = None

	def connect(self):
		self.connection = sqlite3.connect(self.db_name)

	def disconnect(self):
		if self.connection:
			self.connection.close()

	def execute_query(self, query, data=None):
		if not self.connection:
			self.connect()
		cursor = self.connection.cursor()
		if data:
			cursor.execute(query, data)
		else:
			cursor.execute(query)
		self.connection.commit()
		return cursor

	def create_table(self, table_name, columns):
		query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
		self.execute_query(query)

	def insert_data(self, table_name, data):
		placeholders = ', '.join(['?' for _ in data])
		query = f"INSERT INTO {table_name} VALUES ({placeholders})"
		self.execute_query(query, data)


# Example usage:
db_manager = DatabaseManager('du.db')

# Create characters table if not exists
db_manager.create_table('characters', 'username TEXT, email TEXT, password TEXT')

# Insert new data into the characters table
new_character = ("Gandalf", "gandalf@example.com", "you_shall_not_pass")
db_manager.insert_data('characters', new_character)

# Disconnect from the database
db_manager.disconnect()
