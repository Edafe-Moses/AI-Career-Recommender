import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from scipy.sparse import hstack

# Load dataset
DATA_PATH = Path(r"C:\Users\user\Documents\backend\dataset\AI-based Career Recommendation System.csv")
data = pd.read_csv(DATA_PATH)

# Rename for convenience
data.rename(columns=lambda x: x.strip(), inplace=True)

# Drop rows with missing target
data = data.dropna(subset=['Recommended_Career'])

# Select features and target
features = data[['Age', 'Education', 'Skills', 'Interests']].copy()
target = data['Recommended_Career']

# Handle missing values
features['Skills'] = features['Skills'].fillna('')
features['Interests'] = features['Interests'].fillna('')

# Encode education
edu_encoder = LabelEncoder()
features.loc[:, 'Education_enc'] = edu_encoder.fit_transform(features['Education'])

# Combine text features
features.loc[:, 'Text_Features'] = features['Skills'] + " " + features['Interests']

# Vectorize text
vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(features['Text_Features'])

# Combine text vector with other features
X_other = features[['Age', 'Education_enc']].values
X = hstack([X_text, X_other])

# Encode target
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(target)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Predict
y_pred = clf.predict(X_test)

# Labels for report
labels = sorted(list(set(y_train) | set(y_test)))

# Print classification report
print("Classification Report:")
print(classification_report(
    y_test,
    y_pred,
    labels=labels,
    target_names=target_encoder.inverse_transform(labels),
    zero_division=0
))

# Ensure model directory exists
Path("model").mkdir(parents=True, exist_ok=True)

# Save model and encoders
joblib.dump(clf, "model/career_model.pkl")
joblib.dump(edu_encoder, "model/encoder_edu.pkl")
joblib.dump(target_encoder, "model/encoder_target.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model and encoders saved successfully.")
