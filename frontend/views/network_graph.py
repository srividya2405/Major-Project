import streamlit as st
import pandas as pd

from pyvis.network import Network

from utils.api import get_transactions


def get_color(risk_level):

    if risk_level == "High":
        return "#ff3333"

    if risk_level == "Medium":
        return "#ffc107"

    return "#4caf50"


def get_size(risk_level):

    if risk_level == "High":
        return 55

    if risk_level == "Medium":
        return 42

    return 32


def get_edge_width(risk_level):

    if risk_level == "High":
        return 7

    if risk_level == "Medium":
        return 4

    return 2


def show_network_graph():

    st.title("🌐 AML Fraud Network Analyzer")

    data = get_transactions()

    df = pd.DataFrame(data)

    suspicious_df = df[
        df["Risk Level"].isin(["High", "Medium"])
    ].copy()

    if suspicious_df.empty:

        st.warning("No suspicious transactions found.")

        return

    suspicious_df = suspicious_df.sort_values(
        by="Risk Score",
        ascending=False
    ).head(25)

    total_suspicious = len(suspicious_df)

    high_count = len(
        suspicious_df[
            suspicious_df["Risk Level"] == "High"
        ]
    )

    medium_count = len(
        suspicious_df[
            suspicious_df["Risk Level"] == "Medium"
        ]
    )

    suspicious_banks = set(
        suspicious_df["From Bank"].astype(str)
    ).union(
        set(
            suspicious_df["To Bank"].astype(str)
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Suspicious Transactions",
        total_suspicious
    )

    c2.metric(
        "High Risk Links",
        high_count
    )

    c3.metric(
        "Medium Risk Links",
        medium_count
    )

    c4.metric(
        "Suspicious Banks",
        len(suspicious_banks)
    )

    st.markdown(
        """
### Legend

🔴 High Risk Bank  
🟡 Medium Risk Bank  
➡️ Arrow shows money transfer direction
"""
    )

    net = Network(
        height="720px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#222222"
    )

    net.barnes_hut(
        gravity=-7000,
        central_gravity=0.25,
        spring_length=260,
        spring_strength=0.035,
        damping=0.1
    )

    for _, row in suspicious_df.iterrows():

        from_bank = f"Bank {row['From Bank']}"
        to_bank = f"Bank {row['To Bank']}"
        risk_level = row["Risk Level"]
        amount_paid = row["Amount Paid"]
        amount_received = row["Amount Received"]
        score = row["Risk Score"]
        payment_format = row["Payment Format"]

        color = get_color(risk_level)
        size = get_size(risk_level)
        edge_width = get_edge_width(risk_level)

        net.add_node(
            from_bank,
            label=from_bank,
            color=color,
            size=size,
            title=(
                f"<b>{from_bank}</b><br>"
                f"Risk Level: {risk_level}<br>"
                f"Risk Score: {score}"
            )
        )

        net.add_node(
            to_bank,
            label=to_bank,
            color=color,
            size=size,
            title=(
                f"<b>{to_bank}</b><br>"
                f"Risk Level: {risk_level}<br>"
                f"Risk Score: {score}"
            )
        )

        net.add_edge(
            from_bank,
            to_bank,
            color=color,
            width=edge_width,
            arrows="to",
            title=(
                f"<b>Suspicious Transaction Flow</b><br>"
                f"From: {from_bank}<br>"
                f"To: {to_bank}<br>"
                f"Amount Paid: {amount_paid:,.2f}<br>"
                f"Amount Received: {amount_received:,.2f}<br>"
                f"Payment Format: {payment_format}<br>"
                f"Risk Score: {score}<br>"
                f"Risk Level: {risk_level}"
            )
        )

    html_content = net.generate_html()

    st.iframe(
        html_content,
        width="stretch",
        height=760
    )

    st.info(
        "This graph visualizes AI-detected suspicious transaction flows. Red nodes show high-risk entities and yellow nodes show medium-risk entities."
    )
