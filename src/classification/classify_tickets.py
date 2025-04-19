'''
Task was to classify the issue description into one of the categories,I have used BERT embeddings and Logistic Regression.
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
import re
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    doc = nlp(text)
    lemmatized = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return lemmatized

nlp = spacy.load("en_core_web_sm")

# 1. Load dataset
df = pd.read_csv("C:\\Users\\kalya\\OneDrive\\Desktop\\Crayon Data\\Data\\Data.csv")
print(df['category'].value_counts())

df['cleaned_description'] = df['issue_description'].apply(preprocess)
X = df['cleaned_description']
y = df['category']

# 2. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 3. Load BERT model for sentence embeddings
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# 4. Convert text to BERT embeddings
X_train_bert = bert_model.encode(X_train.tolist(), convert_to_numpy=True, show_progress_bar=True)
X_test_bert = bert_model.encode(X_test.tolist(), convert_to_numpy=True, show_progress_bar=True)

# 5. SMOTE on BERT embeddings
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train_bert, y_train)

# 6. Train classifier
clf = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
clf.fit(X_resampled, y_resampled)

# 7. Predict and evaluate
y_pred = clf.predict(X_test_bert)

# 8. Results
results = pd.DataFrame({
    'issue_description': X_test,
    'true_category': y_test,
    'predicted_category': y_pred
})
print(results.head())

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# 9. Save the model and BERT model
model_path = "classifier_model.pkl"
with open(model_path, 'wb') as f:
    pickle.dump(clf, f)
bert_model.save("bert_model")

print(f"Model saved to {model_path}")

# 10. Function to predict a single instance (for FastAPI integration)
def predict_category(issue_description, clf, bert_model):
    cleaned_desc = preprocess(issue_description)
    vector = bert_model.encode([cleaned_desc], convert_to_numpy=True)
    prediction = clf.predict(vector)[0]
    return prediction