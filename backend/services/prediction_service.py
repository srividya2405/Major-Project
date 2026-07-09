import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import joblib
import torch
import torch.nn as nn
import pandas as pd

from config import (
    SCALER_PATH,
    RECEIVING_ENCODER_PATH,
    PAYMENT_ENCODER_PATH,
    FORMAT_ENCODER_PATH,
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


isolation_model = joblib.load(ISOLATION_MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

receiving_encoder = joblib.load(RECEIVING_ENCODER_PATH)

payment_encoder = joblib.load(PAYMENT_ENCODER_PATH)

format_encoder = joblib.load(FORMAT_ENCODER_PATH)

autoencoder = Autoencoder(12)

autoencoder.load_state_dict(
    torch.load(
        AUTOENCODER_MODEL_PATH,
        map_location="cpu"
    )
)

autoencoder.eval()


def predict_transaction(transaction):

    row = pd.DataFrame([transaction])

    row["Receiving Currency"] = receiving_encoder.transform(
        row["Receiving Currency"]
    )

    row["Payment Currency"] = payment_encoder.transform(
        row["Payment Currency"]
    )

    row["Payment Format"] = format_encoder.transform(
        row["Payment Format"]
    )

    X = scaler.transform(row)

    isolation_score = -isolation_model.score_samples(X)[0]

    X_tensor = torch.tensor(
        X,
        dtype=torch.float32
    )

    with torch.no_grad():

        reconstructed = autoencoder(X_tensor)

        reconstruction_error = torch.mean(
            (X_tensor - reconstructed) ** 2
        ).item()

    score = (
        isolation_score * 50 +
        reconstruction_error * 50
    )

    score = max(
        0,
        min(
            100,
            score
        )
    )

    if score >= 40:

        risk = "High"

    elif score >= 30:

        risk = "Medium"

    else:

        risk = "Low"

    reasons = []

    if transaction["Amount Paid"] >= 200000000:
        reasons.append("Large transaction amount")

    if transaction["From Bank"] != transaction["To Bank"]:
        reasons.append("Cross-bank transaction")

    if transaction["Payment Format"] in ["Bitcoin", "UPI", "Wire"]:
        reasons.append("High-risk payment method")

    if isolation_score > 0.6:
        reasons.append("High anomaly detected by Isolation Forest")

    if reconstruction_error > 0.5:
        reasons.append("High reconstruction error from Autoencoder")

    if not reasons:
        reasons.append("Transaction pattern appears normal")

    if risk == "High":
        recommendation = "Immediate manual investigation recommended."

    elif risk == "Medium":
        recommendation = "Monitor this transaction carefully."

    else:
        recommendation = "Transaction appears safe."

    return {

        "Risk Score": round(score, 2),

        "Risk Level": risk,

        "Reasons": reasons,

        "Recommendation": recommendation

    }