import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score

def train_and_evaluate(dataset_path='datasets/expertise_dataset.csv', model_dir='ai_model'):
    if not os.path.exists(dataset_path):
        try:
            from ai_model.generate_dataset import generate_synthetic_dataset
        except ImportError:
            from generate_dataset import generate_synthetic_dataset
        generate_synthetic_dataset(output_path=dataset_path)

    print(f"[*] Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    # Text pre-processing and feature extraction
    vectorizer = TfidfVectorizer(max_features=800, ngram_range=(1, 2), stop_words='english')
    X_text = vectorizer.fit_transform(df['skills_text']).toarray()
    
    # Label encoding target domain
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['target_domain'])
    
    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=42, stratify=y)
    
    # Models to compare
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=150, random_state=42, max_depth=20),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=15),
        'Naive Bayes': MultinomialNB(alpha=0.5)
    }
    
    results = {}
    best_model_name = 'Random Forest'
    best_model_obj = None
    best_acc = 0.0
    
    for name, clf in models.items():
        print(f"[*] Training {name} Classifier...")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average='weighted'))
        rec = float(recall_score(y_test, y_pred, average='weighted'))
        f1 = float(f1_score(y_test, y_pred, average='weighted'))
        
        results[name] = {
            'accuracy': round(acc * 100, 2),
            'precision': round(prec * 100, 2),
            'recall': round(rec * 100, 2),
            'f1_score': round(f1 * 100, 2)
        }
        
        print(f"    -> {name} Accuracy: {results[name]['accuracy']}%")
        
        if acc > best_acc:
            best_acc = acc
            best_model_name = name
            best_model_obj = clf
            
    print(f"\n[SUMMARY] Best Performing Model: {best_model_name} ({results[best_model_name]['accuracy']}%)")
    
    # Save artifacts
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(best_model_obj, os.path.join(model_dir, 'expertise_model.pkl'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer.pkl'))
    joblib.dump(label_encoder, os.path.join(model_dir, 'label_encoder.pkl'))
    
    metrics_summary = {
        'best_model': best_model_name,
        'accuracy': results[best_model_name]['accuracy'],
        'models_comparison': results,
        'domain_classes': list(label_encoder.classes_),
        'total_samples': len(df)
    }
    
    with open(os.path.join(model_dir, 'model_metrics.json'), 'w') as f:
        json.dump(metrics_summary, f, indent=4)
        
    print(f"[SUCCESS] Saved model artifacts to {model_dir}/")
    return metrics_summary

if __name__ == '__main__':
    train_and_evaluate()
