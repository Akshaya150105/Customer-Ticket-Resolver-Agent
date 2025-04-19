from sqlalchemy import create_engine, MetaData, Table
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/kalya/OneDrive/Desktop/Crayon Data/src/app/ticket_data.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

metadata = MetaData()
metadata.reflect(bind=engine)
if 'new_tickets' in metadata.tables:
    new_tickets_table = metadata.tables['new_tickets']
    new_tickets_table.drop(engine)
    print("✅ 'new_tickets' table dropped successfully.")
else:
    print("⚠️ 'new_tickets' table not found.")
