from pathlib import Path

# -----------------------------
# Project Root
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent

# -----------------------------
# Dataset Paths
# -----------------------------

RAW_DATASET_PATH = BASE_DIR / "dataset" / "raw" / "HI-Small_Trans.csv"

WORKING_DATASET_PATH = BASE_DIR / "dataset" / "processed" / "working_dataset.csv"

FINAL_DATASET_PATH = BASE_DIR / "dataset" / "processed" / "final_dataset.csv"

TRAINING_DATASET_PATH = BASE_DIR / "dataset" / "processed" / "training_dataset.csv"

# -----------------------------
# AI Model Paths
# -----------------------------

SCALER_PATH = BASE_DIR / "ai" / "training" / "scaler.pkl"

RECEIVING_ENCODER_PATH = BASE_DIR / "ai" / "training" / "receiving_currency_encoder.pkl"

PAYMENT_ENCODER_PATH = BASE_DIR / "ai" / "training" / "payment_currency_encoder.pkl"

FORMAT_ENCODER_PATH = BASE_DIR / "ai" / "training" / "payment_format_encoder.pkl"

ISOLATION_MODEL_PATH = BASE_DIR / "ai" / "isolation_forest" / "isolation_forest.pkl"

AUTOENCODER_MODEL_PATH = BASE_DIR / "ai" / "autoencoder" / "autoencoder.pth"