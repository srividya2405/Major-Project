import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from config import (
    FINAL_DATASET_PATH,
    TRAINING_DATASET_PATH,
    SCALER_PATH,
    ISOLATION_MODEL_PATH
)


def load_dataset():

    return pd.read_csv(FINAL_DATASET_PATH)


def prepare_data(df):

    X = df.drop(columns=["Is Laundering"])

    y = df["Is Laundering"]

    return X, y


def scale_data(X):

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    return X_scaled


def train_model(X_scaled):

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_scaled)

    joblib.dump(
        model,
        ISOLATION_MODEL_PATH
    )


def save_training_dataset(X_scaled, y):

    df = pd.DataFrame(X_scaled)

    df["Is Laundering"] = y.values

    df.to_csv(
        TRAINING_DATASET_PATH,
        index=False
    )

    print(df.shape)

    print("Training dataset created successfully.")


def main():

    df = load_dataset()

    X, y = prepare_data(df)

    X_scaled = scale_data(X)

    train_model(X_scaled)

    save_training_dataset(
        X_scaled,
        y
    )


if __name__ == "__main__":

    main()