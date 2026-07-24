import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib

def calculate_shannon_entropy(text: str) -> float:
    import math
    from collections import Counter
    if not text or not isinstance(text, str):
        return 0.0
    words = text.lower().split()
    total_words = len(words)
    if total_words <= 1:
        return 0.0
    word_counts = Counter(words)
    entropy = -sum((count / total_words) * math.log2(count / total_words) for count in word_counts.values())
    length_penalty = min(1.0, len(text) / 45.0)
    return entropy * length_penalty

def train_and_save_model():
    print("🚀 Loading training dataset...")
    # Load dataset
    df = pd.read_csv("../sample_gcc_orders.csv")
    
    # Feature engineering
    print("⚙️ Computing address entropy features...")
    df['address_entropy'] = df['address_text'].apply(calculate_shannon_entropy)
    
    # Prepare features and labels
    X = df[['address_entropy', 'customer_history_refusals']]
    y = df['rto_status']
    
    print("🎓 Training Random Forest risk classifier...")
    # Train model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Save model
    model_filename = "app/analytics/rto_model.joblib"
    joblib.dump(model, model_filename)
    print(f"✅ Model successfully saved to: {model_filename}")
    
    # Print metrics
    train_accuracy = model.score(X, y)
    print(f"📊 Training Accuracy: {train_accuracy * 100:.2f}%")

if __name__ == "__main__":
    train_and_save_model()
