import sys
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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
        "High Risk": int((df["Risk Level"] == "High").sum()),
        "Medium Risk": int((df["Risk Level"] == "Medium").sum()),
        "Low Risk": int((df["Risk Level"] == "Low").sum())
    }


def get_transactions():

    return get_data().to_dict(
        orient="records"
    )


def get_high_risk():

    df = get_data()

    return df[
        df["Risk Level"] == "High"
    ].to_dict(
        orient="records"
    )


def predict_transaction(data):

    try:

        from backend.services.prediction_service import (
            predict_transaction as run_model_prediction
        )

        return run_model_prediction(data)

    except Exception as error:

        return {
            "error": str(error)
        }
