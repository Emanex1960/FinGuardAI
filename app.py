import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="FinGuard AI", layout="wide")

# -------------------- PREMIUM FINTECH DARK THEME --------------------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}
[data-testid="stMetricValue"] {
    color: #00FFB3;
    font-weight: bold;
}
.stProgress > div > div > div > div {
    background-color: #00FFB3;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# -------------------- LOGIN SYSTEM --------------------
def login():

    st.markdown("<h1 style='text-align: center;'>🔐 FinGuard AI Secure Access</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Enterprise Financial Intelligence Portal</h4>", unsafe_allow_html=True)
    st.markdown("---")

    col1,col2,col3 = st.columns([1,2,1])

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
                st.error("Invalid credentials. Access restricted.")

        st.info("""
Demo Credentials  
Email: admin@finguardai.com  
Password: FinGuard2026
""")


# -------------------- DASHBOARD --------------------
def dashboard():

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # -------------------- HEADER --------------------
    st.title("🔐 FinGuard AI")
    st.subheader("AI-Powered Financial Fraud & Insider Threat Intelligence Platform")
    st.markdown("---")

    # -------------------- SIDEBAR --------------------
    st.sidebar.header("🏢 Company Settings")

    company = st.sidebar.selectbox(
        "Select Company",
        ["GlobalTech Ltd","FinServe Inc","Nova Retail Group"]
    )

    threshold = st.sidebar.slider(
        "High Risk Threshold ($)",
        10000,
        25000,
        18000
    )

    # -------------------- DATA GENERATION --------------------
    @st.cache_data
    def generate_data(threshold):

        users = ["Finance Lead","Accountant","HR Manager","CEO","IT Admin"]
        locations = ["USA","UK","Germany","Nigeria","Canada"]
        departments = ["Finance","HR","IT","Operations","Procurement"]

        data = []

        for i in range(300):

            amount = random.randint(100,25000)
            user = random.choice(users)
            location = random.choice(locations)
            department = random.choice(departments)

            date = datetime.now() - timedelta(days=random.randint(0,120))

            risk = "Low"

            if amount > threshold:
                risk = "High"

            elif amount > threshold * 0.5:
                risk = "Medium"

            data.append([
                i+1,
                user,
                location,
                department,
                amount,
                risk,
                date
            ])

        df = pd.DataFrame(data, columns=[
            "Transaction ID",
            "User Role",
            "Location",
            "Department",
            "Amount ($)",
            "Risk Level",
            "Date"
        ])

        return df


    df = generate_data(threshold)

    # -------------------- FRAUD ANOMALY SCORE --------------------
    df["z_score"] = (df["Amount ($)"] - df["Amount ($)"].mean()) / df["Amount ($)"].std()
    df["Anomaly"] = df["z_score"].abs() > 2


    # -------------------- RISK CALCULATIONS --------------------
    high_risk = len(df[df["Risk Level"]=="High"])
    medium_risk = len(df[df["Risk Level"]=="Medium"])
    low_risk = len(df[df["Risk Level"]=="Low"])

    risk_score = round((high_risk/len(df))*100,2)

    # -------------------- TOP RISK ROLE --------------------
    top_risk_role = df[df["Risk Level"]!="Low"]["User Role"].value_counts().idxmax()

    # -------------------- METRICS --------------------
    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric("Total Transactions",len(df))
    col2.metric("High Risk Transactions",high_risk)
    col3.metric("Medium Risk Transactions",medium_risk)
    col4.metric("Overall Risk Exposure (%)",f"{risk_score}%")
    col5.metric("Most Risky Role",top_risk_role)

    st.markdown("---")

    # -------------------- CFVI CALCULATION --------------------
    base_cfvi = min(100, round((high_risk*1.5 + medium_risk*0.8),2))

    st.sidebar.markdown("### 🧪 CFVI Risk Simulation")

    simulation_adjustment = st.sidebar.slider(
        "Adjust Risk Scenario (%)",
        -50,
        50,
        0
    )

    cfvi = min(100, max(0, base_cfvi + simulation_adjustment))

    if cfvi < 30:
        risk_level_label = "Low Organizational Risk"
    elif cfvi < 60:
        risk_level_label = "Moderate Organizational Risk"
    else:
        risk_level_label = "High Organizational Risk"


    # -------------------- LIVE THREAT ALERT --------------------
    if high_risk > 20:
        st.error("🚨 LIVE THREAT ALERT: Abnormally high volume of suspicious transactions detected!")

    # -------------------- CFVI DISPLAY --------------------
    st.subheader("🧠 Company Fraud Vulnerability Index (CFVI)")

    colA,colB = st.columns(2)

    colA.metric("Organizational Risk Score",f"{cfvi}/100")
    colB.info(risk_level_label)

    st.subheader("📊 Organizational Risk Gauge")

    st.progress(cfvi/100)

    st.markdown("---")

    # -------------------- BOARD INSIGHT --------------------
    potential_leakage = high_risk * threshold

    st.subheader("📌 Board-Level Financial Risk Insight")

    st.warning(
        f"If current high-risk patterns persist, estimated financial exposure may reach **${potential_leakage:,}**."
    )

    st.markdown("---")

    # -------------------- PIE CHART RISK DISTRIBUTION --------------------
    st.subheader("📊 Transaction Risk Distribution")

    risk_counts = df["Risk Level"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        risk_counts.values,
        labels=risk_counts.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig)

    st.markdown("---")

    # -------------------- REGIONAL FRAUD --------------------
    st.subheader("🌍 Regional High-Risk Concentration")

    region_risk = df[df["Risk Level"]=="High"].groupby("Location").size()

    if not region_risk.empty:

        fig2,ax2 = plt.subplots()
        ax2.bar(region_risk.index,region_risk.values)

        st.pyplot(fig2)

    st.markdown("---")

    # -------------------- FLAGGED TRANSACTIONS --------------------
    st.subheader("🚨 Flagged Transactions Intelligence")

    flagged = df[df["Risk Level"]!="Low"]

    search_role = st.selectbox(
        "Filter by User Role",
        ["All"] + list(df["User Role"].unique())
    )

    if search_role != "All":
        flagged = flagged[flagged["User Role"] == search_role]

    st.dataframe(flagged,use_container_width=True)

    st.markdown("---")

    # -------------------- FRAUD PROBABILITY --------------------
    st.subheader("🧠 Fraud Probability Predictor")

    fraud_probability = round((len(flagged)/len(df))*100,2)

    st.metric("Estimated Fraud Probability",f"{fraud_probability}%")

    st.markdown("---")

    # -------------------- STATISTICAL ANOMALIES --------------------
    st.subheader("⚠ Statistical Fraud Anomalies")

    anomalies = df[df["Anomaly"]==True]

    if anomalies.empty:
        st.success("No statistical anomalies detected.")

    else:
        st.dataframe(anomalies,use_container_width=True)

    st.markdown("---")

    # -------------------- FRAUD TREND --------------------
    st.subheader("📈 Fraud Risk Trend Over Time")

    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    monthly_risk = df.groupby("Month")["Amount ($)"].mean().reset_index()

    st.line_chart(monthly_risk.set_index("Month"))

    st.markdown("---")

    # -------------------- FRAUD HEATMAP --------------------
    st.subheader("🔥 Fraud Concentration by Department")

    dept_counts = flagged["Department"].value_counts()

    st.bar_chart(dept_counts)

    st.markdown("---")

    # -------------------- DOWNLOAD REPORT --------------------
    st.download_button(
        "📂 Download Fraud Report",
        df.to_csv(index=False),
        "FinGuard_Fraud_Report.csv",
        "text/csv"
    )


# -------------------- APP ROUTING --------------------
if not st.session_state.authenticated:
    login()
else:
    dashboard()
