"""Streamlit page for simulating logistics: product movement and order fulfillment."""

import streamlit as st
from db.queries import (
    move_product, get_route_cost, get_orders,
    update_order_status, move_order_to_customer,
    get_inventory_for_sku, get_locations,
    get_cheapest_route_details, write_log,
    suggest_cheapest_origin
)

if "role" not in st.session_state or st.session_state.role != "Admin":
    st.error("⛔ Access Denied: Admins only.")
    st.stop()

st.title("🚚 Logistics Simulator")

# --- Manual Movement ---
st.subheader("Manual Product Movement")

origins, destinations = get_locations()

sku = st.text_input("SKU")
destination = st.selectbox("Destination Warehouse", destinations, key="manual_dest")
quantity = st.number_input("Quantity to Move", min_value=1, key="manual_qty")

# Suggest cheapest origin based on transport cost
origin_suggestion = None
if sku and destination:
    origin_suggestion = suggest_cheapest_origin(sku.strip().upper(), destination.strip())
    if origin_suggestion:
        st.caption(
            f"💡 Suggested Origin: {origin_suggestion['origin']} "
            f"(₹{origin_suggestion['cost']:.2f})"
        )

origin = st.selectbox(
    "Origin Warehouse",
    origins,
    index=origins.index(origin_suggestion['origin']) if origin_suggestion else 0,
    key="manual_origin"
)

if sku and origin and destination and quantity:
    route_info = get_cheapest_route_details(origin.strip(), destination.strip())
    if route_info:
        st.caption(
            f"📍 Route Info: ₹{route_info['cost']} for {route_info['distance']} km"
        )

    cost_per_unit = get_route_cost(origin.strip(), destination.strip())
    if cost_per_unit is not None:
        total_cost = cost_per_unit * quantity
        st.info(f"Transport Cost: ₹{total_cost:.2f}")
        if st.button("Simulate Movement"):
            try:
                move_product(
                    sku.strip().upper(),
                    origin.strip(),
                    destination.strip(),
                    quantity,
                    total_cost
                )
                write_log(
                    1,
                    f"Moved {quantity} units of {sku.upper()} from {origin} to {destination}"
                )
                st.success(
                    f"✅ Moved {quantity} units of {sku} from {origin} to {destination}"
                )
            except ValueError as ve:
                st.error(f"Validation error: {ve}")
            except ConnectionError as ce:
                st.error(f"Database error: {ce}")
            except Exception as unexpected:
                st.error(f"Unexpected error: {unexpected.__class__.__name__}")
                raise
    else:
        st.warning("⚠️ No route found between selected origin and destination.")

# --- Move Orders to Customer ---
st.subheader("📦 Move Orders to Customer")

orders = get_orders()
pending_orders = [o for o in orders if o[5] == "Pending"]

if pending_orders:
    st.markdown("### Pending Orders")
    header = st.columns([1.2, 2, 1.2, 2, 2, 2])
    header[0].markdown("**Order ID**")
    header[1].markdown("**SKU**")
    header[2].markdown("**Qty**")
    header[3].markdown("**Customer**")
    header[4].markdown("**Location**")
    header[5].markdown("**Action**")

    for order in pending_orders:
        order_id, sku, qty, customer, location, status = order
        row = st.columns([1.2, 2, 1.2, 2, 2, 2])
        row[0].write(order_id)
        row[1].write(sku)
        row[2].write(qty)
        row[3].write(customer)
        row[4].write(location)

        inventory_sources = get_inventory_for_sku(sku.strip().upper())
        valid_origins = [
            loc for loc, available_qty in inventory_sources
            if available_qty >= qty and not loc.startswith("Retail Hub")
        ]

        if not valid_origins:
            row[5].warning("⚠️ No warehouse has enough stock")
        else:
            origin_suggestion = suggest_cheapest_origin(sku.strip().upper(), location.strip())
            if origin_suggestion:
                row[5].caption(
                    f"💡 Suggested: {origin_suggestion['origin']} "
                    f"(₹{origin_suggestion['cost']:.2f})"
                )

            selected_origin = row[5].selectbox(
                "Origin",
                valid_origins,
                index=valid_origins.index(origin_suggestion['origin'])
                if origin_suggestion and origin_suggestion['origin'] in valid_origins
                else 0,
                key=f"origin_{order_id}"
            )

            route_cost = get_route_cost(selected_origin.strip(), location.strip())
            if route_cost is None:
                row[5].warning("⚠️ No route from origin to customer")
            else:
                if row[5].button("🚚 Move", key=f"move_{order_id}"):
                    try:
                        move_order_to_customer(
                            order_id,
                            sku.strip().upper(),
                            qty,
                            selected_origin.strip(),
                            location.strip()
                        )
                        update_order_status(order_id, "Processed")
                        write_log(
                            1,
                            f"Processed order #{order_id}: {qty} units of {sku.upper()} "
                            f"from {selected_origin} to {location}"
                        )
                        st.success(
                            f"✅ Order #{order_id} moved from {selected_origin} to {location}"
                        )
                        st.rerun()
                    except ValueError as ve:
                        st.error(f"Validation error: {ve}")
                    except ConnectionError as ce:
                        st.error(f"Database error: {ce}")
                    except Exception as unexpected:
                        st.error(f"Unexpected error: {unexpected.__class__.__name__}")
                        raise
else:
    st.info("No pending orders to move.")
