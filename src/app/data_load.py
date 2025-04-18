import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection
db_path = "tickets.db"
engine = create_engine(f"sqlite:///{db_path}")

# Load CSV
csv_path = "C:\\Users\\kalya\\OneDrive\\Desktop\\Crayon Data\\Data\\Data.csv" 
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

df = pd.read_csv(csv_path)

# Ensure column names match the model (case-sensitive)
expected_columns = ['ticket_id', 'customer_id', 'date_created', 'category', 'subcategory', 
                   'priority', 'issue_description', 'resolution', 'resolution_time_hours', 
                   'customer_satisfaction', 'agent_id']
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns in CSV: {missing_columns}")

# Load data into the 'tickets' table
df.to_sql('tickets', engine, if_exists='replace', index=False, dtype={
    'ticket_id': 'TEXT',
    'customer_id': 'TEXT',
    'date_created': 'TEXT',
    'category': 'TEXT',
    'subcategory': 'TEXT',
    'priority': 'TEXT',
    'issue_description': 'TEXT',
    'resolution': 'TEXT',
    'resolution_time_hours': 'TEXT',
    'customer_satisfaction': 'TEXT',
    'agent_id': 'TEXT'
})

print(f"Successfully loaded {len(df)} rows into tickets.db")