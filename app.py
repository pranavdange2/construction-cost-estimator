from openai import OpenAI
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Construction Cost Estimator", page_icon="🏗️")

st.title("🏗️ AI Construction Cost Estimator")
st.write("Estimate project cost and get budget suggestions instantly!")

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

if st.button("Estimate Cost"):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Base rate lookup
    rate_row = rates[rates["Location"].str.lower() == location.lower()]
    if not rate_row.empty:
        base_rate = rate_row[quality].values[0]
    else:
        base_rate = 1600  # default fallback rate

    prompt = f"""
    You are a construction cost estimation expert.
    Estimate the total cost for a {area} sq.ft {project_type} in {location} 
    using {quality} materials at ₹{base_rate} per sq.ft.
    Give a clear breakdown and 3 cost optimization suggestions.
    """

    with st.spinner("Calculating..."):
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

    st.subheader("💰 Estimated Cost & Suggestions")
    st.write(response.choices[0].message.content)

