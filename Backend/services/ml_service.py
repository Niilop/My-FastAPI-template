# backend/services/ml_service.py
import joblib

MODEL_PATH = "models/ml_models/placeholder_model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def predict(data, model):
    return model.predict(data)