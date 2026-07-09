import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

from torch.utils.data import DataLoader, TensorDataset

from config import (
    TRAINING_DATASET_PATH,
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


def load_dataset():

    df = pd.read_csv(
        TRAINING_DATASET_PATH,
        nrows=200000
    )

    X = df.drop(columns=["Is Laundering"])

    return torch.tensor(
        X.values,
        dtype=torch.float32
    )


def train_model(X):

    dataset = TensorDataset(X)

    loader = DataLoader(
        dataset,
        batch_size=512,
        shuffle=True
    )

    model = Autoencoder(X.shape[1])

    criterion = nn.MSELoss()

    optimizer = optim.Adam(
        model.parameters(),
        lr=0.001
    )

    epochs = 10

    for epoch in range(epochs):

        total_loss = 0

        for batch in loader:

            data = batch[0]

            output = model(data)

            loss = criterion(
                output,
                data
            )

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        print(
            f"Epoch {epoch + 1}/{epochs} | Loss: {total_loss / len(loader):.6f}"
        )

    torch.save(
        model.state_dict(),
        AUTOENCODER_MODEL_PATH
    )

    print("\nAutoencoder trained successfully.")


def main():

    X = load_dataset()

    train_model(X)


if __name__ == "__main__":

    main()