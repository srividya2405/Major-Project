import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd

from config import (
    RAW_DATASET_PATH,
    WORKING_DATASET_PATH
)


def load_dataset():

    return pd.read_csv(RAW_DATASET_PATH)


def clean_dataset(df):

    df = df.drop_duplicates()

    df = df.dropna()

    return df


def save_dataset(df):

    df.to_csv(
        WORKING_DATASET_PATH,
        index=False
    )

    print(df.shape)

    print("Working dataset created successfully.")


def main():

    df = load_dataset()

    df = clean_dataset(df)

    save_dataset(df)


if __name__ == "__main__":

    main()