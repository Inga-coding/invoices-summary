import pandas as pd
import streamlit as st

from app.config import INVOICES_FILE
from app.data_loader import load_invoices, parse_invoice_lines
from app.services import calculate_total_amount, get_unpaid_invoices

st.set_page_config(page_title="Звіт по рахунках", layout="wide")

st.title("Звіт по рахунках")
st.info(
    "Оберіть фільтри у бічній панелі ліворуч, щоб проаналізувати суми рахунків, "
    "перевірити неоплачені позиції та переглянути розподіл за клієнтами."
)

st.sidebar.header("Налаштування та фільтри")
uploaded_file = st.sidebar.file_uploader("Завантажити свій CSV (необов'язково)", type="csv")

try:
    if uploaded_file is not None:
        raw_text = uploaded_file.getvalue().decode("utf-8")
        lines = raw_text.splitlines()
        invoices = parse_invoice_lines(lines, strict=False)
    else:
        invoices = load_invoices(INVOICES_FILE, strict=False)

    if not invoices:
        st.warning("Файл порожній або не містить коректних рахунків.")
        st.stop()

    df = pd.DataFrame(invoices)

    clients = ["Усі клієнти"] + sorted(df["client"].unique().tolist())
    selected_client = st.sidebar.selectbox("Клієнт", clients)

    statuses = sorted(df["status"].unique().tolist())
    selected_statuses = st.sidebar.multiselect("Статус рахунку", statuses, default=statuses)

    min_amount_val = int(df["amount"].min())
    max_amount_val = int(df["amount"].max())
    if min_amount_val < max_amount_val:
        min_selected = st.sidebar.slider(
            "Мінімальна сума (грн)",
            min_value=min_amount_val,
            max_value=max_amount_val,
            value=min_amount_val,
        )
    else:
        min_selected = min_amount_val

    filtered_df = df.copy()
    if selected_client != "Усі клієнти":
        filtered_df = filtered_df[filtered_df["client"] == selected_client]

    filtered_df = filtered_df[filtered_df["status"].isin(selected_statuses)]
    filtered_df = filtered_df[filtered_df["amount"] >= min_selected]

    if filtered_df.empty:
        st.warning("За вибраними фільтрами рахунків не знайдено. Спробуйте змінити умови пошуку.")
        st.stop()

    filtered_invoices = filtered_df.to_dict(orient="records")
    total_amount = calculate_total_amount(filtered_invoices)
    unpaid_invoices = get_unpaid_invoices(filtered_invoices)

    col1, col2, col3 = st.columns(3)
    col1.metric("Кількість рахунків", len(filtered_df))
    col2.metric("Загальна сума, грн", f"{total_amount:,.2f}")
    col3.metric("Очікується / прострочено", len(unpaid_invoices))

    st.subheader("Деталізація рахунків")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("Сума рахунків за клієнтами")
    chart_df = filtered_df.groupby("client", as_index=False)["amount"].sum()
    st.bar_chart(chart_df, x="client", y="amount")

except FileNotFoundError as err:
    st.error(f"Файл даних не знайдено: {err}")
    st.stop()
except Exception as err:
    st.error(f"Непередбачена помилка: {err}")
    st.stop()