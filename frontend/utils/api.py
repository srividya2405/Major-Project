from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "predicted_transactions.csv.gz"
)


@st.cache_data(show_spinner=False)
def get_data():

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    return pd.read_csv(
        DATA_PATH,
        compression="gzip"
    )


def get_statistics():

    df = get_data()

    return {

        "Total Transactions": int(len(df)),

        "High Risk": int(
            (df["Risk Level"] == "High").sum()
        ),

        "Medium Risk": int(
            (df["Risk Level"] == "Medium").sum()
        ),

        "Low Risk": int(
            (df["Risk Level"] == "Low").sum()
        )

    }


def get_transactions():

    df = get_data()

    return df.to_dict(
        orient="records"
    )


def get_high_risk():

    df = get_data()

    high_risk_df = df[
        df["Risk Level"] == "High"
    ]

    return high_risk_df.to_dict(
        orient="records"
    )


def predict_transaction(data):

    return {

        "Risk Score": 27.6,

        "Risk Level": "Low",

        "Reasons": [
            "Demo mode prediction on Streamlit Cloud"
        ],

        "Recommendation": (
            "Run locally for full FastAPI model prediction."
        )

    }
