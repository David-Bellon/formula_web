import streamlit as st
import fastf1
from general_functions import get_driver_laps


def render_page(session_number):
    session = fastf1.get_session(2024, session_number, 'R')
    session.load()

    name = "Race Result " + session.session_info["Meeting"]["Name"]
    st.title(name)

    st.title("Driver Laps")
    get_driver_laps(session)
