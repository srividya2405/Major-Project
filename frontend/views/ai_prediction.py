import streamlit as st
from datetime import date, time

from utils.api import predict_transaction


def show_ai_prediction():

    st.title("🤖 AI Transaction Risk Prediction")

    st.write("Enter transaction details and let the trained AI models predict AML risk.")

    col1, col2 = st.columns(2)

    with col1:

        transaction_date = st.date_input(
            "Transaction Date",
            value=date(2022, 9, 1)
        )

        from_bank = st.number_input(
            "From Bank",
            min_value=1,
            value=1
        )

        amount_received = st.number_input(
            "Amount Received",
            min_value=0.0,
            value=1000.0
        )

        receiving_currency = st.selectbox(
            "Receiving Currency",
            [
                "Australian Dollar",
                "Bitcoin",
                "Brazil Real",
                "Canadian Dollar",
                "Euro",
                "Mexican Peso",
                "Ruble",
                "Rupee",
                "Saudi Riyal",
                "Shekel",
                "Swiss Franc",
                "UK Pound",
                "US Dollar",
                "Yen",
                "Yuan"
            ]
        )

    with col2:

        transaction_time = st.time_input(
            "Transaction Time",
            value=time(10, 30)
        )

        to_bank = st.number_input(
            "To Bank",
            min_value=1,
            value=2
        )

        amount_paid = st.number_input(
            "Amount Paid",
            min_value=0.0,
            value=1000.0
        )

        payment_currency = st.selectbox(
            "Payment Currency",
            [
                "Australian Dollar",
                "Bitcoin",
                "Brazil Real",
                "Canadian Dollar",
                "Euro",
                "Mexican Peso",
                "Ruble",
                "Rupee",
                "Saudi Riyal",
                "Shekel",
                "Swiss Franc",
                "UK Pound",
                "US Dollar",
                "Yen",
                "Yuan"
            ]
        )

    payment_format = st.selectbox(
        "Payment Format",
        [
            "ACH",
            "Bitcoin",
            "Cash",
            "Cheque",
            "Credit Card",
            "UPI"
        ]
    )

    if st.button("Predict Risk"):

        backend_payment_format = payment_format

        if payment_format == "UPI":
            backend_payment_format = "Wire"

        payload = {

            "Year": transaction_date.year,
            "Month": transaction_date.month,
            "Day": transaction_date.day,
            "Hour": transaction_time.hour,
            "Minute": transaction_time.minute,

            "From Bank": int(from_bank),
            "To Bank": int(to_bank),

            "Amount Received": float(amount_received),
            "Receiving Currency": receiving_currency,

            "Amount Paid": float(amount_paid),
            "Payment Currency": payment_currency,

            "Payment Format": backend_payment_format

        }

        result = predict_transaction(payload)

        if "Risk Score" not in result:

            st.error("Prediction Failed")

            st.json(result)

            return

        st.divider()

        st.subheader("Prediction Result")

        c1, c2 = st.columns(2)

        c1.metric(
            "Risk Score",
            result["Risk Score"]
        )

        c2.metric(
            "Risk Level",
            result["Risk Level"]
        )

        if result["Risk Level"] == "High":

            st.error("🚨 High Risk Transaction Detected")

        elif result["Risk Level"] == "Medium":

            st.warning("⚠️ Medium Risk Transaction")

        else:

            st.success("✅ Low Risk Transaction")

        st.subheader("AI Decision Explanation")

        for reason in result["Reasons"]:

            st.write("✔️", reason)

        st.subheader("Recommendation")

        st.info(result["Recommendation"])