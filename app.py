import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Hybrid AI Construction Cost Estimator (Simulated)", page_icon="🏗️")
st.title("🏗️ Hybrid AI Construction Cost Estimator (Simulated)")
st.write("Simulates OpenAI and Gemini API calls without real keys.")

# User Inputs
area = st.number_input("Total Area (sq.ft)", min_value=100)
location = st.text_input("Location", "Nashik")
project_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial"])
quality = st.selectbox("Material Quality", ["Basic", "Standard", "Premium"])

# Pre-trained dataset
data = {
    "Location": ["Nashik", "Pune", "Aurangabad"],
    "Basic": [1300, 1400, 1200],
    "Standard": [1700, 1800, 1600],
    "Premium": [2100, 2300, 2000]
}
rates = pd.DataFrame(data)

# Suggestions template
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

# Offline cost estimation
def simulate_estimation(area, location, quality):
    row = rates[rates["Location"].str.lower() == location.lower()]
    rate = row[quality].values[0] if not row.empty else 1600
    total_cost = area * rate
    breakdown = {
        "Foundation & Structure": round(total_cost * 0.35),
        "Masonry & Finishing": round(total_cost * 0.38),
        "Electrical & Plumbing": round(total_cost * 0.18),
        "Miscellaneous": round(total_cost * 0.09),
    }
    suggestions = suggestions_templates.get(quality, [])
    return total_cost, breakdown, suggestions

# Simulated API call function
def simulate_api_call(model_name, prompt):
    st.write(f"Calling {model_name} API...")
    with st.spinner(f"{model_name} generating response..."):
        time.sleep(2)  # simulate network delay
    st.success(f"{model_name} API call completed!")
    # Return pre-generated response
    return f"[Simulated {model_name} Response] Cost estimate and suggestions based on prompt: {prompt}"

# Button
if st.button("Estimate Cost"):
    # Offline estimation
    total, breakdown, suggestions = simulate_estimation(area, location, quality)
    st.subheader(f"💰 Estimated Cost (Offline): ₹{total:,}")
    st.write("### Cost Breakdown")
    for k, v in breakdown.items():
        st.write(f"{k}: ₹{v:,}")
    st.write("### Suggestions")
    for s in suggestions:
        st.write(f"- {s}")

    # Prepare prompt for AI simulation
    prompt = f"Estimate total cost for {area} sq.ft {project_type} in {location} using {quality} materials."

    st.write("---")
    # Simulated OpenAI API
    openai_response = simulate_api_call("OpenAI GPT-4", prompt)
    st.subheader("🤖 OpenAI GPT-4 (Simulated)")
    st.write(openai_response)

    # Simulated Gemini API
    gemini_response = simulate_api_call("Gemini AI", prompt)
    st.subheader("🤖 Gemini AI (Simulated)")
    st.write(gemini_response)

    st.info("Thank You")
