"""Streamlit page for placing, viewing, and managing customer orders."""

import time
import streamlit as st
from db.queries import (
    place_order, get_orders, delete_order, get_customer_locations
)

# --- Access Control ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⛔ Please log in to access this page.")
    st.stop()

st.title("Order Manager")

# --- Place Custom Order ---
st.subheader("Place Custom Order")
sku = st.text_input("SKU")
quantity = st.number_input("Quantity", min_value=1)

if st.session_state.role == "User":
    customer_name = st.session_state.username
    st.text_input("Customer Name", value=customer_name, disabled=True)
else:
    customer_name = st.text_input("Customer Name")

locations = get_customer_locations()
customer_location = st.selectbox("Customer Location", locations)

if st.button("Place Order"):
    try:
        place_order(
            sku.strip().upper(),
            quantity,
            customer_name.strip(),
            customer_location.strip()
        )
        st.success(
            f"✅ Order placed for {quantity} units of {sku} "
            f"by {customer_name} to {customer_location}"
        )
        time.sleep(2.5)
        st.rerun()
    except ValueError as ve:
        st.error(f"Validation error: {ve}")
    except ConnectionError as ce:
        st.error(f"Database error: {ce}")
    except Exception as unexpected:
        st.error(f"Unexpected error: {unexpected.__class__.__name__}")
        raise

# --- Display Orders Based on Role ---
st.subheader("All Orders" if st.session_state.role == "Admin" else "My Orders")
orders = get_orders(st.session_state.username, st.session_state.role)

if orders:
    st.markdown("### 📦 Current Orders")

    header = st.columns([1, 2, 1.5, 2, 2, 1.5, 1.5])
    header[0].markdown("**Order ID**")
    header[1].markdown("**SKU**")
    header[2].markdown("**Qty**")
    header[3].markdown("**Customer**")
    header[4].markdown("**Location**")
    header[5].markdown("**Status**")
    header[6].markdown("**Actions**")

    for order in orders:
        order_id, sku, qty, customer, location, status = order
        row = st.columns([1, 2, 1.5, 2, 2, 1.5, 1.5])
        row[0].write(order_id)
        row[1].write(sku)
        row[2].write(qty)
        row[3].write(customer)
        row[4].write(location)
        row[5].write(status)

        if status == "Pending" and st.session_state.role == "Admin":
            if row[6].button("🗑️ Delete", key=f"delete_{order_id}"):
                try:
                    delete_order(order_id)
                    st.success(f"Order #{order_id} deleted.")
                    st.rerun()
                except ValueError as ve:
                    st.error(f"Validation error: {ve}")
                except ConnectionError as ce:
                    st.error(f"Database error: {ce}")
                except Exception as unexpected:
                    st.error(f"Unexpected error: {unexpected.__class__.__name__}")
                    raise
        else:
            row[6].markdown("✅")
else:
    st.info("No orders found.")
