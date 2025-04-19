import pickle
from sentence_transformers import SentenceTransformer
import os
import re
import spacy

# Load the trained model and BERT model
model_path = r"C:\\Users\\kalya\\OneDrive\\Desktop\\Crayon Data\\src\\classification\\classifier_model.pkl"
bert_path = r"C:\\Users\\kalya\\OneDrive\\Desktop\\Crayon Data\\src\\classification\\bert_model"
with open(model_path, 'rb') as f:
    clf = pickle.load(f)
bert_model = SentenceTransformer(bert_path)

def classify_ticket(issue_description):
    """Classify a new ticket using the trained model."""
    return predict_category(issue_description, clf, bert_model)

def predict_category(issue_description, clf, bert_model):
    """Preprocess and predict category for a single instance."""
    def preprocess(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        doc = nlp(text)
        lemmatized = " ".join([token.lemma_ for token in doc if not token.is_stop])
        return lemmatized
    nlp = spacy.load("en_core_web_sm")
    
    cleaned_desc = preprocess(issue_description)
    vector = bert_model.encode([cleaned_desc], convert_to_numpy=True)
    prediction = clf.predict(vector)[0]
    return prediction