import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import get_transactions


def show_analytics():

    st.title("📊 AI Risk Analytics")

    data = get_transactions()

    df = pd.DataFrame(data)

    st.subheader("Risk Level Distribution")

    fig = px.bar(
        df["Risk Level"].value_counts().reset_index(),
        x="Risk Level",
        y="count",
        color="Risk Level",
        title="AI Predicted Risk Levels"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Payment Format Distribution")

    fig = px.pie(
        df,
        names="Payment Format",
        title="Payment Formats"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Top 10 Banks by Transactions")

    bank_counts = (
        df["From Bank"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    bank_counts.columns = [
        "Bank",
        "Transactions"
    ]

    fig = px.bar(
        bank_counts,
        x="Bank",
        y="Transactions",
        title="Top 10 Sender Banks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )