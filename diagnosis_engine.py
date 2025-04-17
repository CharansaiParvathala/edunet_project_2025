# diagnosis_engine.py

import pickle
import numpy as np
from disease_data import get_disease_info

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("symptom_list.pkl", "rb") as f:
    symptom_list = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

def predict_disease(user_symptoms):
    input_vector = [0] * len(symptom_list)
    for symptom in user_symptoms:
        if symptom in symptom_list:
            idx = symptom_list.index(symptom)
            input_vector[idx] = 1

    prediction = model.predict([input_vector])[0]
    prediction_label = label_encoder.inverse_transform([prediction])[0]

    probs = model.predict_proba([input_vector])[0]
    top_indices = np.argsort(probs)[::-1][:3]
    top_diseases = [(label_encoder.inverse_transform([i])[0], probs[i]) for i in top_indices]

    detailed_results = []
    for disease, score in top_diseases:
        info = get_disease_info(disease)
        detailed_results.append({
            "disease": disease,
            "confidence": round(score * 100, 2),
            "description": info["description"],
            "precautions": info["precautions"],
            "treatment": info["treatment"]
        })

    return detailed_results
      
