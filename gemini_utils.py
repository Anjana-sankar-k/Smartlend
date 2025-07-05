import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Configure your Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_loan_report(summary_dict):
    prompt = f"""
You are a financial assistant tasked with generating a professional gold loan eligibility report based on the following application summary:

{summary_dict}

Provide a clear, well-structured report covering:
1. Applicant Details (Name, DOB, Gender, etc.)
2. Financial Insights (Monthly Income, Risk Level, CIBIL Score)
3. Collateral Info (Gold Weight, Market Price, LTV Ratio, Loan Amount)
4. Final Recommendation on loan approval and risk justification.

Keep the tone formal and consultative.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API error: {e}"
