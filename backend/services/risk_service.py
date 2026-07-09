import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd


df = pd.read_csv(
    "dataset/processed/predicted_transactions.csv"
)


def get_statistics():

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

    return df.to_dict(
        orient="records"
    )


def get_high_risk_transactions():

    return df[
        df["Risk Level"] == "High"
    ].to_dict(
        orient="records"
    )