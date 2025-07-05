import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Set random seed
np.random.seed(42)

# Step 1: Generate synthetic data
num_samples = 1000
income = np.random.randint(10000, 100000, num_samples)
age = np.random.randint(21, 60, num_samples)
cibil = np.random.randint(600, 800, num_samples)
emotional_score = np.random.randint(0, 11, num_samples)

# Define risk label
def determine_risk(inc, ag, cb, emo):
    if cb < 650 and emo < 4:
        return "High"
    elif cb < 700 or inc < 30000:
        return "Medium"
    else:
        return "Low"

risk = [determine_risk(inc, ag, cb, emo) for inc, ag, cb, emo in zip(income, age, cibil, emotional_score)]

# Define dynamic LTV ratio based on score + emotional value
def determine_ltv(cb, emo):
    if cb >= 750:
        return np.random.randint(73, 76)  # high CIBIL
    elif cb >= 700:
        return np.random.randint(70, 74)
    elif cb >= 650:
        return np.random.randint(67, 71) + (emo // 4)
    else:
        return np.random.randint(60, 66) + (emo // 3)  # emo helps low cb

ltv_ratio = [determine_ltv(cb, emo) for cb, emo in zip(cibil, emotional_score)]

# Step 2: Create DataFrame
data = pd.DataFrame({
    "income": income,
    "age": age,
    "cibil": cibil,
    "emotional_score": emotional_score,
    "risk": risk,
    "ltv_ratio": ltv_ratio
})

# Step 3: Encode risk labels
label_map = {"Low": 0, "Medium": 1, "High": 2}
data["risk_label"] = data["risk"].map(label_map)

# Step 4: Split features
X = data[["income", "age", "cibil", "emotional_score"]]

# Train Risk Classifier
y_risk = data["risk_label"]
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X, y_risk, test_size=0.2, random_state=42)
risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
risk_model.fit(X_train_r, y_train_r)

# Train LTV Regressor
y_ltv = data["ltv_ratio"]
X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(X, y_ltv, test_size=0.2, random_state=42)
ltv_model = RandomForestRegressor(n_estimators=100, random_state=42)
ltv_model.fit(X_train_l, y_train_l)

# Step 5: Save models
joblib.dump(risk_model, "risk_model.pkl")
joblib.dump(ltv_model, "ltv_predictor.pkl")

print("✅ Models trained and saved:")
print(" - risk_model.pkl (Risk: Low/Medium/High)")
print(" - ltv_predictor.pkl (LTV ratio %)")
