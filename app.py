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

/* Ticker */
.ticker-container{
width:100%;
overflow:hidden;
background:#111;
border:1px solid #00FFB3;
margin-top:10px;
}

.ticker-text{
display:inline-block;
white-space:nowrap;
padding-left:100%;
animation:ticker 25s linear infinite;
color:#00FFB3;
font-weight:bold;
font-size:16px;
}

@keyframes ticker{
0%{transform:translateX(0);}
100%{transform:translateX(-100%);}
}

/* Threat Pulse */

.threat-box{
background:#0E1117;
border:1px solid #00FFB3;
padding:20px;
margin-top:10px;
text-align:center;
border-radius:10px;
}

.pulse{
width:20px;
height:20px;
background:#00FFB3;
border-radius:50%;
margin:auto;
animation:pulse 1.5s infinite;
}

@keyframes pulse{
0%{
transform:scale(.8);
box-shadow:0 0 0 0 rgba(0,255,179,0.7);
}
70%{
transform:scale(1);
box-shadow:0 0 0 10px rgba(0,255,179,0);
}
100%{
transform:scale(.8);
}
}

.threat-text{
margin-top:10px;
font-size:16px;
font-weight:bold;
color:#00FFB3;
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

    # -------------------- CYBER FRAUD TICKER --------------------

    st.markdown("""
<div class="ticker-container">
<div class="ticker-text">
🚨 CYBER FRAUD ALERT: Suspicious offshore transfer detected | 
⚠ Insider access anomaly in Finance Department | 
🛡 AI Monitoring 300+ Transactions in Real-Time | 
📡 FinGuard Threat Intelligence Engine Active | 
🔎 Behavioral anomaly detected in executive account
</div>
</div>
""", unsafe_allow_html=True)

    # -------------------- THREAT DETECTION ANIMATION --------------------

    st.markdown("""
<div class="threat-box">
<div class="pulse"></div>
<div class="threat-text">
LIVE AI THREAT DETECTION ENGINE MONITORING TRANSACTIONS
</div>
</div>
""", unsafe_allow_html=True)

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

    cfvi_slider = st.sidebar.slider(
        "Fraud Vulnerability Simulation (CFVI)",
        0,
        100,
        50
    )

    # -------------------- DATA GENERATION --------------------

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

    # -------------------- RISK CALCULATIONS --------------------

    high_risk = len(df[df["Risk Level"]=="High"])
    medium_risk = len(df[df["Risk Level"]=="Medium"])
    low_risk = len(df[df["Risk Level"]=="Low"])

    risk_score = round((high_risk/len(df))*100,2)

    # -------------------- CFVI --------------------

    base_cfvi = min(100, round((high_risk*1.2 + medium_risk*0.6),2))

    cfvi = round((base_cfvi * 0.6) + (cfvi_slider * 0.4),2)

    cfvi = min(100, cfvi)

    if cfvi < 30:
        risk_level_label = "Low Organizational Risk"
    elif cfvi < 60:
        risk_level_label = "Moderate Organizational Risk"
    else:
        risk_level_label = "High Organizational Risk"

    # -------------------- LIVE ALERT --------------------

    if high_risk > 20:
        st.error("🚨 LIVE THREAT ALERT: Abnormally high volume of suspicious transactions detected!")

    # -------------------- METRICS --------------------

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Transactions",len(df))
    col2.metric("High Risk Transactions",high_risk)
    col3.metric("Medium Risk Transactions",medium_risk)
    col4.metric("Overall Risk Exposure (%)",f"{risk_score}%")

    st.markdown("---")

    # -------------------- CFVI --------------------

    st.subheader("🧠 Company Fraud Vulnerability Index (CFVI)")

    colA,colB = st.columns(2)

    colA.metric("Organizational Risk Score",f"{cfvi}/100")

    colB.info(risk_level_label)

    # -------------------- RISK GAUGE --------------------

    st.subheader("📊 Organizational Risk Gauge")

    st.progress(cfvi/100)

    if cfvi < 35:
        st.success(f"🟢 Low Risk Level ({cfvi}/100)")
    elif cfvi < 65:
        st.warning(f"🟡 Moderate Risk Level ({cfvi}/100)")
    else:
        st.error(f"🔴 High Risk Level ({cfvi}/100)")

    st.markdown("---")

    # -------------------- FLAGGED TRANSACTIONS --------------------

    st.subheader("🚨 Flagged Transactions Intelligence")

    flagged = df[df["Risk Level"]!="Low"]

    st.dataframe(flagged,use_container_width=True)

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
