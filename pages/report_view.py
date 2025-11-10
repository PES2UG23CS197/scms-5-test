"""Streamlit page for viewing summary metrics and logistics movement analytics."""

import streamlit as st
from db.queries import generate_summary_report, get_logistics_records


def handle_streamlit_error(error: Exception):
    """Display appropriate Streamlit error messages."""
    if isinstance(error, ValueError):
        st.error(f"Validation error: {error}")
    elif isinstance(error, ConnectionError):
        st.error(f"Database error: {error}")
    else:
        st.error(f"Unexpected error: {error.__class__.__name__}")
        raise error


# --- Access Control ---
if "role" not in st.session_state or st.session_state.role != "Admin":
    st.error("⛔ Access Denied: Admins only.")
    st.stop()

st.title("📊 Reports & Analytics")

# --- Summary Metrics ---
try:
    report = generate_summary_report()

    st.metric("Total Orders", report["Total Orders"])
    st.metric("Processed Orders", report["Processed Orders"])
    st.metric("Low Stock Items", report["Low Stock Items"])
    st.metric("Total Logistics Cost (₹)", f"{report['Total Logistics Cost']:.2f}")

    # --- Logistics Cost Table ---
    st.subheader("📦 Logistics Movements")

    logistics = get_logistics_records()

    if logistics:
        logistics_table = []
        LOGISTICS_COST_TOTAL = 0  # pylint: disable=C0103

        for record in logistics:
            sku, origin, destination, cost = record
            logistics_table.append({
                "SKU": sku,
                "From": origin,
                "To": destination,
                "Cost (₹)": f"{cost:.2f}",
            })
            LOGISTICS_COST_TOTAL += cost

        st.table(logistics_table)
        st.success(f"🧾 Total Logistics Cost: ₹{LOGISTICS_COST_TOTAL:.2f}")
    else:
        st.info("No logistics records found.")

except Exception as unexpected:  # noqa: BLE001
    handle_streamlit_error(unexpected)
