import random
import threading
import time

import requests
import streamlit as st
from collector_core import FINGERPRINT
from collector_core.daemon import CollectorCore
from collector_core.mcu import MCU

st.set_page_config(
    page_title="Collector Dashboard",
    page_icon=":bar_chart:",
)

core = CollectorCore()
thread = threading.Thread(target=core.main_thread)
thread.start()


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


@st.dialog(title="Add new MCU")
def add_mcu():
    options = ["Real", "Fake"]
    selection = st.pills("MCU Type", options, selection_mode="single")

    if selection == "Real":
        st.text("Not Implemented")

    if selection == "Fake":
        mcu_name = st.text_input("MCU Name")
        if st.button("Add"):
            create_mcu(
                name=mcu_name,
                description="0xDEADBEEF",
                type=MCU.MCU_Type.FAKE,
                connection_type=MCU.MCU_ConnectionType.USB,
                is_connected=True,
                dev_id=random.randint(0, 0xFFFFFFFF),
            )
            st.rerun()


st.session_state.api_connected, st.session_state.api_ping = ping_api()
st.sidebar.title("Collector")
api_connection_status()


st.markdown("# MCU Dashboard")
st.button("Add MCU", on_click=add_mcu)
# st.dataframe(get_mcus(), hide_index=True)
thread.join()
