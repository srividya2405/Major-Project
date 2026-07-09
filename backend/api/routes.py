from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.risk_service import (
    get_statistics,
    get_transactions,
    get_high_risk_transactions
)

from backend.services.prediction_service import (
    predict_transaction
)

router = APIRouter()


class TransactionInput(BaseModel):

    Year: int
    Month: int
    Day: int
    Hour: int
    Minute: int

    From_Bank: int = Field(alias="From Bank")
    To_Bank: int = Field(alias="To Bank")

    Amount_Received: float = Field(alias="Amount Received")
    Receiving_Currency: str = Field(alias="Receiving Currency")

    Amount_Paid: float = Field(alias="Amount Paid")
    Payment_Currency: str = Field(alias="Payment Currency")

    Payment_Format: str = Field(alias="Payment Format")

    class Config:

        populate_by_name = True


@router.get("/health")
async def health():

    return {
        "status": "FinGuard API is running successfully"
    }


@router.get("/statistics")
async def statistics():

    return get_statistics()


@router.get("/transactions")
async def transactions():

    return get_transactions()


@router.get("/high-risk")
async def high_risk():

    return get_high_risk_transactions()


@router.post("/predict-risk")
async def predict(data: TransactionInput):

    transaction = {

        "Year": data.Year,
        "Month": data.Month,
        "Day": data.Day,
        "Hour": data.Hour,
        "Minute": data.Minute,

        "From Bank": data.From_Bank,
        "To Bank": data.To_Bank,

        "Amount Received": data.Amount_Received,
        "Receiving Currency": data.Receiving_Currency,

        "Amount Paid": data.Amount_Paid,
        "Payment Currency": data.Payment_Currency,

        "Payment Format": data.Payment_Format

    }

    return predict_transaction(transaction)