import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulated AI Construction Cost Estimator", page_icon="🏗️")
st.title("🏗️ Simulated AI Construction Cost Estimator")
st.write("Estimate construction costs using pre-trained data (offline simulation). No API keys needed.")

# User Inputs
area = st.number_input("Total Area (sq.ft)", min_value=100)
location = st.text_input("Location", "Nashik")
project_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial"])
quality = st.selectbox("Material Quality", ["Basic", "Standard", "Premium"])

# Pre-trained / pre-generated dataset for simulation
data = {
    "Location": ["Nashik", "Pune", "Aurangabad"],
    "Basic": [1300, 1400, 1200],
    "Standard": [1700, 1800, 1600],
    "Premium": [2100, 2300, 2000]
}
rates = pd.DataFrame(data)

# Simulated AI suggestion templates
suggestions_templates = {
    "Basic": [
        "Use local materials to reduce transport cost.",
        "Consider minimizing decorative finishes to save cost.",
        "Optimize layout to reduce wastage of materials."
    ],
    "Standard": [
        "Select standard materials for better durability-cost balance.",
        "Optimize labor allocation to save time and cost.",
        "Use modular design components to reduce construction time."
    ],
    "Premium": [
        "Consider bulk purchasing of premium materials for discounts.",
        "Reduce luxury finishes in non-essential areas.",
        "Optimize project scheduling to save on labor costs."
    ]
}

# Offline cost estimation function
def simulate_estimation(area, location, quality):
    row = rates[rates["Location"].str.lower() == location.lower()]
    if not row.empty:
        rate = row[quality].values[0]
    else:
        rate = 1600  # default fallback

    total_cost = area * rate
    breakdown = {
        "Foundation & Structure": round(total_cost * 0.35),
        "Masonry & Finishing": round(total_cost * 0.38),
        "Electrical & Plumbing": round(total_cost * 0.18),
        "Miscellaneous": round(total_cost * 0.09),
    }

    suggestions = suggestions_templates.get(quality, [])
    return total_cost, breakdown, suggestions

# Button to estimate cost
if st.button("Estimate Cost"):
    total, breakdown, suggestions = simulate_estimation(area, location, quality)
    
    st.subheader(f"💰 Estimated Cost: ₹{total:,}")
    st.write("### Cost Breakdown")
    for k, v in breakdown.items():
        st.write(f"{k}: ₹{v:,}")
    
    st.write("### Suggestions")
    for s in suggestions:
        st.write(f"- {s}")

    st.write("---")
    st.info("This is a **simulated AI response** using pre-trained data. No real API call is made.")
