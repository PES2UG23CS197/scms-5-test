"""Streamlit app for SCMS Dashboard: login, registration, and role-based access."""

import streamlit as st
from db.queries import validate_user, create_user

st.set_page_config(page_title="SCMS Dashboard", layout="wide")

# Optional: Hide default sidebar header
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"]::before {
        content: "";
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.username = None

# Login screen
if not st.session_state.logged_in:
    st.title("🔐 Login to SCMS")

    # --- Login Form ---
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(username.strip(), password.strip())
        if user:
            st.session_state.logged_in = True
            st.session_state.role = user["role"]
            st.session_state.user_id = user["user_id"]
            st.session_state.username = username.strip()
            st.success(f"Welcome {username} ({user['role']})")
            st.rerun()
        else:
            st.error("Invalid credentials")

    # --- Registration Form ---
    st.markdown("---")
    st.subheader("🆕 Create a New Account")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        if new_username and new_password:
            try:
                create_user(new_username.strip(), new_password.strip())
                st.success("✅ Account created successfully. You can now log in.")
            except ValueError as ve:
                st.error(f"Validation error: {ve}")
            except ConnectionError as ce:
                st.error(f"Database connection failed: {ce}")
            except Exception as unexpected:
                st.error(f"Unexpected error: {unexpected.__class__.__name__}")
                raise  # Optional: re-raise for debugging or logging
        else:
            st.warning("Please enter both username and password.")


# Main dashboard
else:
    st.title("Supply Chain Management Simulator")

    # ✅ Show login info on main screen
    st.markdown(f"**Logged in as:** `{st.session_state.username}`")
    st.markdown(f"**Role:** `{st.session_state.role}`")

    # ✅ Logout button on main screen
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # Optional: Sidebar navigation hint
    st.sidebar.success("Use the sidebar to navigate")
