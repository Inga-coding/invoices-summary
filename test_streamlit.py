import pandas as pd
import streamlit as st

from app.data_loader import load_invoices
from app.services import calculate_total_amount, get_unpaid_invoices

st.set_page_config(page_title="Рахунки — Streamlit", layout="wide")

st.title("Звіт по рахунках")
st.write("Перший застосунок на Streamlit поверх логіки проєкту.")

invoices = load_invoices()

if invoices:
    df = pd.DataFrame(invoices)

    total = calculate_total_amount(invoices)
    unpaid = get_unpaid_invoices(invoices)

    st.write(f"**Загальна сума рахунків:** {total}")
    st.write(f"**Кількість неоплачених/прострочених:** {len(unpaid)}")

    st.dataframe(df)

    if "amount" in df.columns:
        x_col = "client" if "client" in df.columns else df.columns[0]
        st.bar_chart(df, x=x_col, y="amount")
else:
    st.warning("Дані рахунків не завантажилися або список порожній.")