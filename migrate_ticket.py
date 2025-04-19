import sqlite3

# Path to your SQLite database
db_path = "C://Users//kalya//OneDrive//Desktop//Crayon Data//src//app//ticket_data.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Turn off foreign key constraints temporarily
    cursor.execute("PRAGMA foreign_keys=off;")
    cursor.execute("BEGIN TRANSACTION;")

    # Rename the old table
    cursor.execute("ALTER TABLE new_tickets RENAME TO new_tickets_old;")

    # Create the new table with updated schema
    cursor.execute("""
    CREATE TABLE new_tickets (
        ticket_id VARCHAR(10) PRIMARY KEY,
        issue_description TEXT,
        category VARCHAR(50),
        status VARCHAR(20) DEFAULT 'Pending',
        draft_resolution TEXT,
        final_resolution TEXT,
        resolution_time_hours VARCHAR(10),
        submission_time DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Copy old data
    cursor.execute("""
    INSERT INTO new_tickets (ticket_id, issue_description, category, status)
    SELECT ticket_id, issue_description, category, status FROM new_tickets_old;
    """)

    # Drop the old table
    cursor.execute("DROP TABLE new_tickets_old;")

    # Commit changes
    conn.commit()
    print("Migration successful!")

except Exception as e:
    conn.rollback()
    print("Migration failed:", e)

finally:
    cursor.execute("PRAGMA foreign_keys=on;")
    conn.close()
