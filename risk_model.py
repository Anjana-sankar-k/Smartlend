import pandas as pd
import joblib

# Load models
risk_model = joblib.load("risk_model.pkl")
ltv_model = joblib.load("ltv_predictor.pkl")

label_map = {0: "Low", 1: "Medium", 2: "High"}

def ml_risk_predictor(income, age, cibil, emotional_score):
    X = pd.DataFrame([{
        "income": float(income),
        "age": int(age),
        "cibil": int(cibil),
        "emotional_score": float(emotional_score)
    }])
    risk = risk_model.predict(X)[0]
    return label_map.get(risk, "Unknown")

def ml_ltv_predictor(income, age, cibil, emotional_score):
    X = pd.DataFrame([{
        "income": float(income),
        "age": int(age),
        "cibil": int(cibil),
        "emotional_score": float(emotional_score)
    }])
    model = joblib.load("ltv_predictor.pkl")
    return round(model.predict(X)[0])
