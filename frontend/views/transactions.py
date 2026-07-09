import streamlit as st
import pandas as pd

from utils.api import get_transactions


def show_transactions():

    st.title("📋 Transaction History Search")

    data = get_transactions()

    df = pd.DataFrame(data)

    st.subheader("Search & Filter Transactions")

    col1, col2, col3 = st.columns(3)

    with col1:

        from_bank = st.text_input("Search From Bank")

    with col2:

        to_bank = st.text_input("Search To Bank")

    with col3:

        risk_level = st.selectbox(
            "Risk Level",
            ["All", "Low", "Medium", "High"]
        )

    col4, col5 = st.columns(2)

    with col4:

        min_amount = st.number_input(
            "Minimum Amount Paid",
            min_value=0.0,
            value=0.0
        )

    with col5:

        max_amount = st.number_input(
            "Maximum Amount Paid",
            min_value=0.0,
            value=float(df["Amount Paid"].max())
        )

    filtered_df = df.copy()

    if from_bank:

        filtered_df = filtered_df[
            filtered_df["From Bank"].astype(str).str.contains(
                from_bank,
                case=False,
                na=False
            )
        ]

    if to_bank:

        filtered_df = filtered_df[
            filtered_df["To Bank"].astype(str).str.contains(
                to_bank,
                case=False,
                na=False
            )
        ]

    if risk_level != "All":

        filtered_df = filtered_df[
            filtered_df["Risk Level"] == risk_level
        ]

    filtered_df = filtered_df[
        (filtered_df["Amount Paid"] >= min_amount) &
        (filtered_df["Amount Paid"] <= max_amount)
    ]

    st.write(f"Showing {len(filtered_df):,} transactions")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600
    )