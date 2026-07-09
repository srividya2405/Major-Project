import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

from config import (
    WORKING_DATASET_PATH,
    FINAL_DATASET_PATH,
    RECEIVING_ENCODER_PATH,
    PAYMENT_ENCODER_PATH,
    FORMAT_ENCODER_PATH
)


def load_dataset():

    return pd.read_csv(WORKING_DATASET_PATH)


def process_timestamp(df):

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Day"] = df["Timestamp"].dt.day
    df["Hour"] = df["Timestamp"].dt.hour
    df["Minute"] = df["Timestamp"].dt.minute

    df.drop(columns=["Timestamp"], inplace=True)

    return df


def encode_columns(df):

    receiving_encoder = LabelEncoder()
    payment_encoder = LabelEncoder()
    format_encoder = LabelEncoder()

    df["Receiving Currency"] = receiving_encoder.fit_transform(
        df["Receiving Currency"]
    )

    df["Payment Currency"] = payment_encoder.fit_transform(
        df["Payment Currency"]
    )

    df["Payment Format"] = format_encoder.fit_transform(
        df["Payment Format"]
    )

    joblib.dump(
        receiving_encoder,
        RECEIVING_ENCODER_PATH
    )

    joblib.dump(
        payment_encoder,
        PAYMENT_ENCODER_PATH
    )

    joblib.dump(
        format_encoder,
        FORMAT_ENCODER_PATH
    )

    return df


def create_dataset(df):

    return df[[
        "Year",
        "Month",
        "Day",
        "Hour",
        "Minute",
        "From Bank",
        "To Bank",
        "Amount Received",
        "Receiving Currency",
        "Amount Paid",
        "Payment Currency",
        "Payment Format",
        "Is Laundering"
    ]]


def save_dataset(df):

    df.to_csv(
        FINAL_DATASET_PATH,
        index=False
    )

    print(df.shape)

    print("Final dataset created successfully.")


def main():

    df = load_dataset()

    df = process_timestamp(df)

    df = encode_columns(df)

    df = create_dataset(df)

    save_dataset(df)


if __name__ == "__main__":

    main()