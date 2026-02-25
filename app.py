import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="FinGuard AI", layout="wide")

st.title("🔐 FinGuard AI")
st.subheader("AI-Powered Financial Fraud & Insider Threat Intelligence Platform")

st.markdown("Enterprise-grade transaction monitoring for global SMEs.")
st.markdown("---")

# Sidebar
st.sidebar.header("Company Settings")
company = st.sidebar.selectbox("Select Company", ["GlobalTech Ltd", "FinServe Inc", "Nova Retail Group"])
threshold = st.sidebar.slider("High Risk Threshold ($)", 10000, 25000, 18000)

# Generate Simulated Data
def generate_data(threshold):
    users = ["Finance Lead", "Accountant", "HR Manager", "CEO", "IT Admin"]
    locations = ["USA", "UK", "Germany", "Nigeria", "Canada"]

    data = []
    for i in range(300):
        amount = random.randint(100, 25000)
        user = random.choice(users)
        location = random.choice(locations)

        risk = "Low"
        if amount > threshold:
            risk = "High"
        elif amount > threshold * 0.5:
            risk = "Medium"

        data.append([i+1, user, location, amount, risk])

    df = pd.DataFrame(data, columns=["Transaction ID", "User Role", "Location", "Amount ($)", "Risk Level"])
    return df

df = generate_data(threshold)

# Risk Score Calculation
high_risk = len(df[df["Risk Level"] == "High"])
risk_score = round((high_risk / len(df)) * 100, 2)

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", len(df))
col2.metric("High Risk Transactions", high_risk)
col3.metric("Medium Risk Transactions", len(df[df["Risk Level"] == "Medium"]))
col4.metric("Overall Risk Score (%)", f"{risk_score}%")

st.markdown("---")

# Risk Chart
st.subheader("📊 Risk Distribution Overview")

risk_counts = df["Risk Level"].value_counts()

fig, ax = plt.subplots()
ax.bar(risk_counts.index, risk_counts.values)
ax.set_ylabel("Number of Transactions")
ax.set_xlabel("Risk Level")
st.pyplot(fig)

st.markdown("---")

# Flagged Transactions
st.subheader("🚨 Flagged Transactions Intelligence")

flagged = df[df["Risk Level"] != "Low"]
st.dataframe(flagged)

st.markdown("---")

if st.button("Generate Executive Risk Report"):
    st.success(f"Executive Risk Report for {company} Generated Successfully!")