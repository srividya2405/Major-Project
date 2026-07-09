import streamlit as st
import pandas as pd

from utils.api import get_high_risk


def show_high_risk():

    st.title("🚨 High Risk Transactions")

    data = get_high_risk()

    df = pd.DataFrame(data)

    st.subheader("AI Detected High Risk Transactions")

    if df.empty:

        st.success("No High Risk Transactions Found.")

        return

    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )

    st.write(f"Total High Risk Transactions : {len(df):,}")