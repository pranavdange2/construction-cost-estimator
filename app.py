import streamlit as st
import pandas as pd
import time
import random

st.set_page_config(page_title="AI Construction Cost Estimator", page_icon="🏗️")
st.title("🏗️ AI Construction Cost Estimator")
st.write("Estimate construction project costs using AI-powered recommendations.")

# ----------------------
# User Inputs
# ----------------------
area = st.number_input("Total Area (sq.ft)", min_value=100, step=50)
location = st.text_input("Location", "Nashik")
project_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial"])
quality = st.selectbox("Material Quality", ["Basic", "Standard", "Premium"])

# ----------------------
# Local dataset for cost calculation
# ----------------------
data = {
    "Location": ["Nashik", "Pune", "Aurangabad"],
    "Basic": [1300, 1400, 1200],
    "Standard": [1700, 1800, 1600],
    "Premium": [2100, 2300, 2000]
}
rates = pd.DataFrame(data)

suggestions_templates = {
    "Basic": [
        "Use local materials to reduce transport costs.",
        "Minimize decorative finishes to save on budget.",
        "Optimize layout to reduce material wastage."
    ],
    "Standard": [
        "Select standard materials for cost-efficiency and durability.",
        "Optimize labor allocation to save time and cost.",
        "Use modular design components to reduce construction time."
    ],
    "Premium": [
        "Consider bulk purchasing of premium materials for discounts.",
        "Reduce luxury finishes in non-essential areas.",
        "Optimize project scheduling to minimize labor costs."
    ]
}

# ----------------------
# Cost estimation
# ----------------------
def estimate_cost(area, location, quality):
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

# ----------------------
# Simulated API call
# ----------------------
def api_call(model_name, prompt):
    st.write(f"Calling {model_name} API...")
    with st.spinner(f"{model_name} processing request..."):
        time.sleep(random.uniform(1.5, 2.5))
    st.success(f"{model_name} response received!")
    # Generate realistic AI-style response
    fake_total = random.randint(95, 105) * area * (
        rates[quality][rates['Location'].str.lower() == location.lower()].values[0]
        if not rates[rates['Location'].str.lower() == location.lower()].empty else 1600
    ) // 100
    response_text = f"""
**Estimated Cost ({model_name}):** ₹{fake_total:,}

**Cost Breakdown:**
- Foundation & Structure: ₹{round(fake_total*0.35):,}
- Masonry & Finishing: ₹{round(fake_total*0.38):,}
- Electrical & Plumbing: ₹{round(fake_total*0.18):,}
- Miscellaneous: ₹{round(fake_total*0.09):,}

**AI Suggestions:**
- Optimize material usage.
- Consider alternative materials to save cost.
- Efficient scheduling to reduce labor expense.
"""
    return response_text

# ----------------------
# Main
# ----------------------
if st.button("Estimate Cost"):
    total, breakdown, suggestions = estimate_cost(area, location, quality)
    
    st.subheader(f"💰 Estimated Cost (Local Calculation): ₹{total:,}")
    st.write("### Cost Breakdown")
    for k, v in breakdown.items():
        st.write(f"{k}: ₹{v:,}")
    
    st.write("### Suggestions")
    for s in suggestions:
        st.write(f"- {s}")

    prompt = f"Estimate total cost for {area} sq.ft {project_type} in {location} using {quality} materials."

    st.write("---")
    st.subheader("🤖 OpenAI GPT-4")
    st.markdown(api_call("OpenAI GPT-4", prompt))
    
    st.subheader("🤖 Gemini AI")
    st.markdown(api_call("Gemini AI", prompt))
