import pandas as pd


DATA_PATH = "dataset/processed/predicted_transactions.csv"


def get_data():

    return pd.read_csv(DATA_PATH)


def get_statistics():

    df = get_data()

    return {

        "Total Transactions": int(len(df)),

        "High Risk": int((df["Risk Level"] == "High").sum()),

        "Medium Risk": int((df["Risk Level"] == "Medium").sum()),

        "Low Risk": int((df["Risk Level"] == "Low").sum())

    }


def get_transactions():

    df = get_data()

    return df.to_dict(orient="records")


def get_high_risk():

    df = get_data()

    return df[df["Risk Level"] == "High"].to_dict(orient="records")


def predict_transaction(data):

    return {

        "Risk Score": 27.6,

        "Risk Level": "Low",

        "Reasons": ["Demo mode prediction on Streamlit Cloud"],

        "Recommendation": "Run locally for full FastAPI model prediction."

    }
