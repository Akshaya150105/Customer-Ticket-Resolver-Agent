
import sqlite3
db_path = "C://Users//kalya//OneDrive//Desktop//Crayon Data//src//app//ticket_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("ALTER TABLE new_tickets ADD COLUMN confirmed_category TEXT;")

conn.commit()
conn.close()
