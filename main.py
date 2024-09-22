import streamlit as st
import pandas as pd
import fastf1
import plotly.graph_objects as go

st.title("My First Streamlit Webpage")

session = fastf1.get_session(2024, 15, 'Q')
session.load()

ver_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('HAM').pick_fastest()

ver_tel = ver_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()

ver_data = ver_tel[["Distance", "Speed"]]
ham_data = ham_tel[["Distance", "Speed"]]
df = pd.DataFrame(columns=["Distance", "Speed_1", "Speed_2"])
df["Distance"] = ver_data["Distance"]
df["Speed_1"] = ver_data["Speed"]
df["Speed_2"] = ham_data["Speed"]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=ham_data["Distance"],
    y=ham_data["Speed"],
    mode="lines",
    name="HAM",
    line=dict(color="red")
))

fig.add_trace(go.Scatter(
    x=ver_data["Distance"],
    y=ver_data["Speed"],
    mode="lines",
    name="VER",
    line=dict(color="blue")
))

fig.update_layout(title="Comparation", xaxis_title="Distance", yaxis_title="Speed")

st.plotly_chart(fig)