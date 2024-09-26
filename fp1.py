import streamlit as st
import fastf1
from general_functions import get_standings_table, get_top_sectors, get_driver_laps, get_driver_tel


def render_page(session_number):
    st.markdown("""
            <style>
                .centered {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                }
        </style>
    """, unsafe_allow_html=True)
    session = fastf1.get_session(2024, session_number, 'FP1')
    session.load()

    name = "FP1 " + session.session_info["Meeting"]["Name"]
    st.title(name)

    table = get_standings_table(session)

    st.table(table)

    st.title("Best Sectors")
    get_top_sectors(session)

    st.title("Telemetry")
    st.markdown("Here you can view the Telemetry of the drivers you select. The lap that is shown is the fastest lap of "
            "each driver. It shows two graphs, the first one is the speed of the car and the bottom one is the RPMs "
            "throw out the lap. Just pick as many drivers as you want and enjoy", unsafe_allow_html=True)
    get_driver_tel(session)

    st.title("Driver Laps")
    st.markdown(
        "Here you can get all the laps in the session from the selected drivers. With this you can get a great view"
        " of pace if is a Free Practice Session or how the pace from the race went", unsafe_allow_html=True)
    get_driver_laps(session)

