from flask import Flask, request, jsonify
import joblib
import numpy as np
from scipy.sparse import hstack, csr_matrix
from pathlib import Path

app = Flask(__name__)

# Correct relative path to model files
MODEL_DIR = Path(r"C:\Users\user\Documents\backend\backend\model\model")
model = joblib.load(MODEL_DIR / "career_model.pkl")
edu_encoder = joblib.load(MODEL_DIR / "encoder_edu.pkl")
target_encoder = joblib.load(MODEL_DIR / "encoder_target.pkl")
vectorizer = joblib.load(MODEL_DIR / "vectorizer.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    age = data.get('Age')
    education = data.get('Education')
    skills = data.get('Skills', '')
    interests = data.get('Interests', '')

    # Encode education
    education_enc = edu_encoder.transform([education])[0]

    # Combine skills and interests
    text_input = skills + " " + interests
    text_features = vectorizer.transform([text_input])

    # Combine numeric and text features
    numeric_features = np.array([[age, education_enc]])
    X_input = hstack([text_features, csr_matrix(numeric_features)])

    # Predict
    prediction = model.predict(X_input)
    recommended_career = target_encoder.inverse_transform(prediction)[0]

    return jsonify({'Recommended_Career': recommended_career})

if __name__ == '__main__':
    app.run(debug=True)
