# src/app/similarity.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sqlalchemy import create_engine, text
import os

# Database URL
DATABASE_URL = "sqlite:///C:/Users/kalya/OneDrive/Desktop/CRAYON DATA/src/app/ticket_data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS index path
index_path = "C:\\Users\\kalya\\OneDrive\\Desktop\\CRAYON DATA\\src\\Data\\tickets_index.faiss"
index = None
df = None

def initialize_index():
    """Initialize FAISS index with existing tickets from the 'tickets' table."""
    global index, df
    
    query = text("SELECT ticket_id, issue_description, category, resolution,priority FROM tickets")
    df = pd.read_sql(query, engine)
    if df.empty: 
        print("No tickets found in the database.")
        return None, df
    corpus = df['issue_description'].tolist()
    corpus_embeddings = model.encode(corpus, convert_to_tensor=False)
    embeddings_np = np.array(corpus_embeddings).astype('float32')

    # Create or update FAISS index
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    return index, df

def get_similar_tickets(issue_description: str, top_k: int = 3):
    """Find similar tickets based on issue_description using FAISS index of existing tickets."""
    global index, df
    # Initialize index if not done
    if index is None or df is None:
        index, df = initialize_index()
        if index is None or df.empty:
            return []

    # Encode the query (new ticket's issue_description)
    query_embedding = model.encode([issue_description], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')
    distances, indices = index.search(query_embedding, top_k)

    similar_tickets = []
    for i, idx in enumerate(indices[0]):
        if idx < len(df):  # Ensure index is valid
            ticket_data = df.iloc[idx].to_dict()
            similarity_score = 100 - distances[0][i]  # Convert distance to similarity (approximate)
            similar_tickets.append({
                "ticket_id": ticket_data.get('ticket_id', 'N/A'),
                "issue_description": ticket_data['issue_description'],
                "category": ticket_data.get('category', 'N/A'),
                "resolution": ticket_data.get('resolution', 'N/A'),
                "priority": ticket_data.get('priority', 'N/A'),
                "similarity_score": similarity_score
            })
    return similar_tickets[:top_k]  # Return top_k results