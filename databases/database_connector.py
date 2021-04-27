from sqlite3 import connect

database_path = "databases/database.sqlite"

conn = connect(database_path, check_same_thread=False)
cursor = conn.cursor()
