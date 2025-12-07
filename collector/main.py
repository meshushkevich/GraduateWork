import time

import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from collector import API_REFRESH_INTERVAL_MS, FINGERPRINT

st.set_page_config(
    page_title="Collector Dashboard",
    page_icon=":bar_chart:",
)


st_autorefresh(interval=API_REFRESH_INTERVAL_MS, key="api_refresh")


def ping_api() -> tuple[bool, float]:
    try:
        start = time.perf_counter()
        r = requests.get("http://your-api-host/ping", timeout=1)
        ping = time.perf_counter() - start
        return r.status_code == 200, ping
    except Exception:
        return False, 0.0


def api_connection_status():
    st.sidebar.subheader("API Status")
    label, color = (
        ("Connected", "green")
        if st.session_state.api_connected
        else ("Disconnected", "red")
    )
    st.sidebar.badge(label=label, color=color)

    st.sidebar.subheader("API Ping")
    label, color = (
        (f"{st.session_state.api_ping:.2f} ms", "green")
        if st.session_state.api_connected
        else ("Unreachable", "red")
    )
    st.sidebar.badge(label=label, color=color)

    st.sidebar.subheader("Machine Fingerprint")
    st.sidebar.badge(label=FINGERPRINT, color="blue")


st.session_state.api_connected, st.session_state.api_ping = ping_api()
st.sidebar.title("Collector")
api_connection_status()


st.markdown("# Dashboard")
