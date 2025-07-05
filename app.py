import streamlit as st
from parse_docs import parse_uploaded_documents
from risk_model import ml_risk_predictor, ml_ltv_predictor
from gemini_utils import generate_loan_report
from datetime import datetime

st.title("💼 Gold Loan Eligibility & Risk Assessment")

# Helper to calculate age from DOB string
def calculate_age(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
        today = datetime.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except:
        return 30  # Fallback

# Step 1: Upload multiple documents
uploaded_files = st.file_uploader(
    "Upload Aadhaar, PAN, or Bank Statement (multiple allowed)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Store parsed result
parsed_data = {}

if uploaded_files:
    st.success("✅ Documents Uploaded Successfully")
    parsed_data = parse_uploaded_documents(uploaded_files)
    st.subheader("🔍 Extracted Information:")
    st.json(parsed_data)

# Step 2: User Inputs
st.markdown("### 📋 Additional Inputs")
cibil_score = st.number_input("Enter CIBIL Score", min_value=300, max_value=900, value=700)
emotional_score = st.slider("Emotional Dependency Score (0 - 10)", 0, 10, 5)

# Step 3: Gold collateral
st.markdown("### 🪙 Gold Collateral Details")
gold_weight = st.number_input("Total weight of gold (in grams)", min_value=0.0, step=0.1)
market_price = st.number_input("Current market price of gold (₹ per gram)", min_value=0)

# Step 4: Risk + LTV Assessment
dob = parsed_data.get("DOB")
income = parsed_data.get("Monthly Income")

if income and dob:
    age = calculate_age(dob)
    risk_level = ml_risk_predictor(income, age, cibil_score, emotional_score)
    ltv_ratio = ml_ltv_predictor(income, age, cibil_score, emotional_score)

    loan_amount = gold_weight * market_price * (ltv_ratio / 100) if gold_weight and market_price else 0

    st.markdown("### 📊 ML-Based Assessment")
    st.write({
        "Name": parsed_data.get("Name"),
        "Age": age,
        "CIBIL Score": cibil_score,
        "Monthly Income": income,
        "Emotional Score": emotional_score,
        "Risk Level": risk_level,
        "Predicted LTV Ratio (%)": ltv_ratio,
        "Eligible Loan Amount": f"₹ {loan_amount:,.2f}"
    })
else:
    age = None
    risk_level = "Unknown"
    ltv_ratio = 0
    loan_amount = 0
    st.warning("⚠️ Required fields (DOB or Income) missing. Risk/LTV analysis skipped.")

# Step 5: Final Summary
st.markdown("### 📝 Final Application Summary")
st.json({
    "Name": parsed_data.get("Name"),
    "DOB": parsed_data.get("DOB"),
    "Gender": parsed_data.get("Gender"),
    "Email": parsed_data.get("Email"),
    "Phone": parsed_data.get("Phone"),
    "Aadhaar Number": parsed_data.get("Aadhaar Number"),
    "Monthly Income": income,
    "Age": age,
    "CIBIL Score": cibil_score,
    "Emotional Dependency Score": emotional_score,
    "Gold Weight (g)": gold_weight,
    "Market Price (₹/g)": market_price,
    "Predicted LTV Ratio (%)": ltv_ratio,
    "Eligible Loan Amount": f"₹ {loan_amount:,.2f}",
    "Risk Level": risk_level
})

# Step 6: AI Report
if st.button("🧠 Generate AI Report"):
    with st.spinner("Generating Gemini AI report..."):
        report = generate_loan_report({
            "Name": parsed_data.get("Name"),
            "DOB": parsed_data.get("DOB"),
            "Gender": parsed_data.get("Gender"),
            "Email": parsed_data.get("Email"),
            "Phone": parsed_data.get("Phone"),
            "Aadhaar Number": parsed_data.get("Aadhaar Number"),
            "Monthly Income": income,
            "Age": age,
            "CIBIL Score": cibil_score,
            "Emotional Dependency Score": emotional_score,
            "Risk Level": risk_level,
            "Gold Weight (g)": gold_weight,
            "Market Price (₹/g)": market_price,
            "Predicted LTV Ratio (%)": ltv_ratio,
            "Eligible Loan Amount": f"₹ {loan_amount:,.2f}",
        })

    st.subheader("📝 Gemini AI Report")
    st.markdown(report)
