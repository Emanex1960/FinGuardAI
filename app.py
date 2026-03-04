import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="FinGuard AI", layout="wide")

# -------------------- SESSION STATE --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -------------------- LOGIN SYSTEM --------------------
def login():

    st.markdown("<h1 style='text-align: center;'>🔐 FinGuard AI Secure Access</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Enterprise Financial Intelligence Portal</h4>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.subheader("Authorized Personnel Login")

        username = st.text_input("Company Email")
        password = st.text_input("Password", type="password")

        if st.button("Login Securely"):
            if username == "admin@finguardai.com" and password == "FinGuard2026":
                st.session_state.authenticated = True
                st.success("Authentication Successful. Redirecting to dashboard...")
                st.rerun()
            else:
                st.error("Invalid credentials. Access restricted to authorized personnel.")

        st.markdown("---")
        st.info("Demo Credentials:\nEmail: admin@finguardai.com\nPassword: FinGuard2026")


# -------------------- DASHBOARD --------------------
def dashboard():

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # -------------------- HEADER --------------------
    st.title("🔐 FinGuard AI")
    st.subheader("AI-Powered Financial Fraud & Insider Threat Intelligence Platform")
    st.markdown("Enterprise-grade transaction monitoring for global SMEs.")
    st.markdown("---")

    # -------------------- SIDEBAR --------------------
    st.sidebar.header("🏢 Company Settings")
    company = st.sidebar.selectbox(
        "Select Company",
        ["GlobalTech Ltd", "FinServe Inc", "Nova Retail Group"]
    )

    threshold = st.sidebar.slider(
        "High Risk Threshold ($)",
        10000, 25000, 18000
    )

    # -------------------- DATA GENERATION --------------------
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

        df = pd.DataFrame(
            data,
            columns=[
                "Transaction ID",
                "User Role",
                "Location",
                "Amount ($)",
                "Risk Level"
            ]
        )

        return df

    df = generate_data(threshold)

    # -------------------- RISK CALCULATIONS --------------------
    high_risk = len(df[df["Risk Level"] == "High"])
    medium_risk = len(df[df["Risk Level"] == "Medium"])
    low_risk = len(df[df["Risk Level"] == "Low"])
    risk_score = round((high_risk / len(df)) * 100, 2)

    # -------------------- METRICS --------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", len(df))
    col2.metric("High Risk Transactions", high_risk)
    col3.metric("Medium Risk Transactions", medium_risk)
    col4.metric("Overall Risk Exposure (%)", f"{risk_score}%")

    st.markdown("---")

    # -------------------- RISK DISTRIBUTION CHART --------------------
    st.subheader("📊 Risk Distribution Overview")

    risk_counts = df["Risk Level"].value_counts()
    colors = ["green", "orange", "red"]

    fig, ax = plt.subplots()
    ax.bar(risk_counts.index, risk_counts.values, color=colors)
    ax.set_ylabel("Number of Transactions")
    ax.set_xlabel("Risk Level")
    ax.set_title("Transaction Risk Classification")

    st.pyplot(fig)

    st.markdown("---")

    # -------------------- FLAGGED TRANSACTIONS --------------------
    st.subheader("🚨 Flagged Transactions Intelligence")

    flagged = df[df["Risk Level"] != "Low"]
    st.dataframe(flagged, use_container_width=True)

    st.markdown("---")

    # -------------------- EXECUTIVE REPORT --------------------
    if st.button("Generate Executive Risk Report"):
        st.success(f"Executive Risk Report for {company} Generated Successfully!")
        st.info("High-risk transactions require immediate review and compliance validation.")


# -------------------- APP ROUTING --------------------
if not st.session_state.authenticated:
    login()
else:
    dashboard()
