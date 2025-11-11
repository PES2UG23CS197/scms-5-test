"""Streamlit page for managing demand forecasts and inventory gap analysis."""

from datetime import date
import streamlit as st
from db.queries import get_forecast, add_forecast, get_inventory_for_forecast

if "role" not in st.session_state or st.session_state.role != "Admin":
    st.error("⛔ Access Denied: Admins only.")
    st.stop()

st.title("📈 Demand Forecast")

# --- Add Forecast ---
st.subheader("Add Forecast")
sku = st.text_input("SKU")
forecast_value = st.number_input("Forecast Quantity", min_value=1)
forecast_date = st.date_input("Forecast Date", value=date.today())

if st.button("Add Forecast"):
    try:
        add_forecast(sku.strip().upper(), forecast_value, forecast_date)
        st.success(f"✅ Forecast added for {sku.upper()} on {forecast_date}")
    except ValueError as ve:
        st.error(f"Validation error: {ve}")
    except ConnectionError as ce:
        st.error(f"Database connection failed: {ce}")
    except Exception as unexpected:
        st.error(f"Unexpected error: {unexpected.__class__.__name__}")
        raise

# --- Forecasted Demand Table ---
st.subheader("📊 Forecasted Demand")
forecasts = get_forecast()

if forecasts:
    forecast_table = []
    for f in forecasts:
        sku, forecast_qty, f_date = f
        current_inventory = get_inventory_for_forecast(sku)
        gap = forecast_qty - current_inventory
        status = "OK" if gap <= 0 else "⚠️ Shortage"

        forecast_table.append({
            "SKU": sku,
            "Forecast Qty": forecast_qty,
            "Date": f_date,
            "Current Inventory": current_inventory,
            "Gap": gap,
            "Status": status
        })

    st.table(forecast_table)
else:
    st.info("No forecast data available.")
