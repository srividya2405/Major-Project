import requests


API_URL = "http://127.0.0.1:8000"


def get_statistics():

    return requests.get(
        f"{API_URL}/statistics"
    ).json()


def get_transactions():

    return requests.get(
        f"{API_URL}/transactions"
    ).json()


def get_high_risk():

    return requests.get(
        f"{API_URL}/high-risk"
    ).json()


def predict_transaction(data):

    response = requests.post(
        f"{API_URL}/predict-risk",
        json=data
    )

    return response.json()