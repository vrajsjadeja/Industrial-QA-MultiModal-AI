"""
Week 2: Classical Machine Learning Baselines
Industrial Application: Predicting hardware failure using Random Forests on tabular sensor data.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def create_synthetic_dataset(samples=1000):
    """Generates synthetic dataset for machine learning training."""
    np.random.seed(42)
    
    # Normal operation data
    temp_normal = np.random.normal(70, 5, int(samples * 0.8))
    vib_normal = np.random.normal(20, 3, int(samples * 0.8))
    status_normal = np.zeros(int(samples * 0.8))
    
    # Failing operation data
    temp_fail = np.random.normal(95, 8, int(samples * 0.2))
    vib_fail = np.random.normal(45, 6, int(samples * 0.2))
    status_fail = np.ones(int(samples * 0.2))
    
    df = pd.DataFrame({
        'temperature_c': np.concatenate([temp_normal, temp_fail]),
        'vibration_hz': np.concatenate([vib_normal, vib_fail]),
        'failure_status': np.concatenate([status_normal, status_fail])
    })
    
    return df.sample(frac=1).reset_index(drop=True)

def main():
    print("🧠 ML Baseline Module: Training Random Forest Classifier...")
    
    df = create_synthetic_dataset()
    X = df[['temperature_c', 'vibration_hz']]
    y = df['failure_status']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    clf.fit(X_train, y_train)
    
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    
    print(f"\n✅ Model Training Complete. Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, predictions, target_names=['Normal', 'Failure']))

if __name__ == "__main__":
    main()
