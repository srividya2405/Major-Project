import streamlit as st
import pandas as pd
import time

from utils.api import get_statistics
from utils.api import get_transactions

from views.transactions import show_transactions
from views.high_risk import show_high_risk
from views.analytics import show_analytics
from views.network_graph import show_network_graph
from views.ai_prediction import show_ai_prediction


st.set_page_config(
    page_title="FinGuard AML Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.sidebar.title("🛡️ FinGuard AML")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Transactions",
        "High Risk",
        "Analytics",
        "Network Graph",
        "AI Prediction"
    ]
)

if page == "Dashboard":

    stats = get_statistics()

    st.title("🛡️ FinGuard AML Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Transactions",
        f"{stats['Total Transactions']:,}"
    )

    c2.metric(
        "High Risk",
        f"{stats['High Risk']:,}"
    )

    c3.metric(
        "Medium Risk",
        f"{stats['Medium Risk']:,}"
    )

    c4.metric(
        "Low Risk",
        f"{stats['Low Risk']:,}"
    )

    st.divider()

    st.subheader("📡 Live AML Transaction Stream")

    data = get_transactions()
    df = pd.DataFrame(data)

    if "live_transactions" not in st.session_state:
        st.session_state.live_transactions = []

    if st.button("▶ Simulate New Transaction"):

        sample = df.sample(1).iloc[0]

        with st.spinner("Processing transaction..."):
            time.sleep(0.8)

        st.session_state.live_transactions.insert(0, sample)

        if len(st.session_state.live_transactions) > 10:
            st.session_state.live_transactions.pop()

    if len(st.session_state.live_transactions) > 0:

        for tx in st.session_state.live_transactions:

            risk = tx["Risk Level"]

            if risk == "High":
                emoji = "🔴"
            elif risk == "Medium":
                emoji = "🟡"
            else:
                emoji = "🟢"

            st.markdown(
                f"""
**{emoji} {risk}**

🕒 **Time:** {int(tx['Hour']):02d}:{int(tx['Minute']):02d}

🏦 **Bank:** {tx['From Bank']} ➜ {tx['To Bank']}

💰 **Amount:** {tx['Amount Paid']:,.2f}

---
"""
            )

    else:

        st.info("No live transactions yet. Click 'Simulate New Transaction'.")

    st.divider()

    st.subheader("System Status")

    st.success("🟢 AI Models Loaded Successfully")

    st.write("Isolation Forest : ✅")

    st.write("Autoencoder : ✅")

elif page == "Transactions":

    show_transactions()

elif page == "High Risk":

    show_high_risk()

elif page == "Analytics":

    show_analytics()

elif page == "Network Graph":

    show_network_graph()

elif page == "AI Prediction":

    show_ai_prediction()