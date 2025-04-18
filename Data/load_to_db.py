import pandas as pd
from sqlalchemy import create_engine, String, Text
import os

# Database connection
db_path = "C:/Users/kalya/OneDrive/Desktop/Crayon Data/src/app/ticket_data.db"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

# Load CSV
csv_path = "C:/Users/kalya/OneDrive/Desktop/Crayon Data/Data/Data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

df = pd.read_csv(csv_path)

# Ensure column names match the model
expected_columns = ['ticket_id', 'customer_id', 'date_created', 'category', 'subcategory', 
                   'priority', 'issue_description', 'resolution', 'resolution_time_hours', 
                   'customer_satisfaction', 'agent_id']
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns in CSV: {missing_columns}")

# Define dtype using SQLAlchemy types
dtype = {
    'ticket_id': String(10),
    'customer_id': String(10),
    'date_created': String(10),
    'category': String(50),
    'subcategory': String(50),
    'priority': String(10),
    'issue_description': Text,
    'resolution': Text,
    'resolution_time_hours': String(10),
    'customer_satisfaction': String(10),
    'agent_id': String(10)
}

# Load data into the 'tickets' table, replacing existing data
df.to_sql('tickets', engine, if_exists='replace', index=False, dtype=dtype)

print(f"Successfully loaded {len(df)} rows into the 'tickets' table in {db_path}")