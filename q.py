import streamlit as st
import fastf1
from general_functions import get_standings_table, get_top_sectors, get_driver_tel


def render_page(session_number):
    session = fastf1.get_session(2024, session_number, 'Q')
    session.load()

    name = "Quali Results " + session.session_info["Meeting"]["Name"]
    st.title(name)

    table = get_standings_table(session)

    st.table(table)

    st.title("Best Sectors")
    get_top_sectors(session)

    st.title("Telemetry")
    get_driver_tel(session)