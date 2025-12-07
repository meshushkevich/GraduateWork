import streamlit as st


def api_connection_status():
    if st.session_state.api_connected:
        st.badge(label="API Connected", color="green")
    else:
        st.badge(label="API Disconnected", color="red")


def sidebar():
    st.sidebar.title("Collector")
    api_connection_status()
