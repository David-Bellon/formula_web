import streamlit as st
import pandas as pd
import fastf1
import plotly.graph_objects as go


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


st.markdown('<h1 class="centered">HOW TO USE THE PAGE</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered">First, select the GP you want to check the data for. Then, '
            'select the session you want to check. Thats it!</p>', unsafe_allow_html=True)
st.markdown('<h3 class="centered">ENJOY AND HOPE YOU LIKE IT</h3>', unsafe_allow_html=True)
