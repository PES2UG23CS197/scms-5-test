"""Streamlit page for viewing inventory levels and low stock alerts."""

import streamlit as st
from db.queries import get_inventory, get_low_stock

if "role" not in st.session_state or st.session_state.role != "Admin":
    st.error("⛔ Access Denied: Admins only.")
    st.stop()

st.title("📦 Inventory Overview")

# --- Organize inventory by location ---
inventory = get_inventory()
location_map = {}

for item in inventory:
    sku = item[1]
    location = item[2]
    quantity = item[3]
    threshold = item[4]
    name = item[5]

    if location not in location_map:
        location_map[location] = []
    location_map[location].append((sku, name, quantity, threshold))

# --- Display inventory by location ---
st.subheader("Inventory by Location")

warehouse_locations = sorted([loc for loc in location_map if not loc.startswith("Retail Hub")])
retail_locations = sorted([loc for loc in location_map if loc.startswith("Retail Hub")])
sorted_locations = warehouse_locations + retail_locations

for location in sorted_locations:
    items = location_map[location]
    st.markdown(f"### {location}")
    table_data = []

    is_retail_hub = location.startswith("Retail Hub")

    for sku, name, qty, threshold in items:
        if is_retail_hub:
            table_data.append({
                "SKU": sku,
                "Product Name": name,
                "Quantity": qty
            })
        else:
            STATUS = "Low" if qty < threshold else "OK"
            table_data.append({
                "SKU": sku,
                "Product Name": name,
                "Quantity": qty,
                "Threshold": threshold,
                "Status": STATUS
            })

    st.table(table_data)

# --- Low Stock Alerts ---
st.subheader("Low Stock Alerts")
low_stock = get_low_stock()
if low_stock:
    for item in low_stock:
        st.error(
            f"{item[1]} ({item[0]}) at {item[2]} is low: {item[3]} units (Threshold: {item[4]})"
        )
else:
    st.success("All inventory levels are sufficient.")
