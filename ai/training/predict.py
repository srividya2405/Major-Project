import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import joblib
import torch
import torch.nn as nn
import pandas as pd

from config import (
    TRAINING_DATASET_PATH,
    FINAL_DATASET_PATH,
    ISOLATION_MODEL_PATH,
    AUTOENCODER_MODEL_PATH
)


class Autoencoder(nn.Module):

    def __init__(self, input_dim):

        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU()
        )

        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )

    def forward(self, x):

        return self.decoder(self.encoder(x))


isolation_model = joblib.load(
    ISOLATION_MODEL_PATH
)

autoencoder = Autoencoder(12)

autoencoder.load_state_dict(
    torch.load(
        AUTOENCODER_MODEL_PATH,
        map_location="cpu"
    )
)

autoencoder.eval()


def main():

    training_df = pd.read_csv(
        TRAINING_DATASET_PATH,
        nrows=200000
    )

    display_df = pd.read_csv(
        FINAL_DATASET_PATH,
        nrows=200000
    )

    X = training_df.drop(
        columns=["Is Laundering"]
    )

    X_scaled = X.values

    isolation_scores = -isolation_model.score_samples(
        X_scaled
    )

    X_tensor = torch.tensor(
        X_scaled,
        dtype=torch.float32
    )

    with torch.no_grad():

        reconstructed = autoencoder(
            X_tensor
        )

        reconstruction_errors = torch.mean(
            (X_tensor - reconstructed) ** 2,
            dim=1
        ).numpy()

    risk_scores = (
        isolation_scores * 50 +
        reconstruction_errors * 50
    )

    risk_scores = risk_scores.clip(
        0,
        100
    )

    risk_levels = []

    for score in risk_scores:

        if score >= 80:

            risk_levels.append("High")

        elif score >= 50:

            risk_levels.append("Medium")

        else:

            risk_levels.append("Low")

    display_df["Risk Score"] = risk_scores.round(2)

    display_df["Risk Level"] = risk_levels

    display_df.to_csv(
        "dataset/processed/predicted_transactions.csv",
        index=False
    )

    print("\nPrediction completed successfully.\n")

    print(display_df["Risk Level"].value_counts())


if __name__ == "__main__":

    main()