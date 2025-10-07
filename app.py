import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Construction Cost Estimator", page_icon="🏗️")

st.title("🏗️ AI Construction Cost Estimator")
st.write("Estimate project cost and get smart budget suggestions using Gemini AI!")

# User Inputs
area = st.number_input("Total Area (sq.ft)", min_value=100)
location = st.text_input("Location", "Nashik")
project_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial"])
quality = st.selectbox("Material Quality", ["Basic", "Standard", "Premium"])

# Load local dataset (optional)
data = {
    "Location": ["Nashik", "Pune", "Aurangabad"],
    "Basic": [1300, 1400, 1200],
    "Standard": [1700, 1800, 1600],
    "Premium": [2100, 2300, 2000]
}
rates = pd.DataFrame(data)

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if st.button("Estimate Cost"):
    # Base rate lookup
    rate_row = rates[rates["Location"].str.lower() == location.lower()]
    if not rate_row.empty:
        base_rate = rate_row[quality].values[0]
    else:
        base_rate = 1600  # fallback rate

    prompt = f"""
    You are a construction cost estimation expert.
    Estimate the total cost for a {area} sq.ft {project_type} in {location}
    using {quality} materials at ₹{base_rate} per sq.ft.
    Provide:
    1️⃣ Total cost
    2️⃣ Cost breakdown (labor, materials, finishing)
    3️⃣ 3 optimization suggestions to reduce cost.
    """

    with st.spinner("Generating AI-based estimation..."):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

    st.subheader("💰 Estimated Cost & Suggestions")
    st.write(response.text)
