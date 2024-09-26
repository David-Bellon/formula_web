from fastf1.core import Laps
import pandas as pd
import streamlit as st
import fastf1.plotting
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_standings_table(session):
    drivers = pd.unique(session.laps["Driver"])
    fastest_laps = []
    for driver in drivers:
        fast_lap = session.laps.pick_driver(driver).pick_fastest()
        if not pd.isna(fast_lap["Driver"]):
            fastest_laps.append(fast_lap)

    fastest_laps = Laps(fastest_laps).sort_values(by="LapTime").reset_index(drop=True)
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps["Difference"] = fastest_laps["LapTime"] - pole_lap["LapTime"]
    fastest_laps["LapTime"] = fastest_laps["LapTime"].apply(lambda x: ":".join(str(x)[:-3].split(":")[1:]))
    fastest_laps["Sector1Time"] = fastest_laps["Sector1Time"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))
    fastest_laps["Sector2Time"] = fastest_laps["Sector2Time"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))
    fastest_laps["Sector3Time"] = fastest_laps["Sector3Time"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))
    fastest_laps["Difference"] = fastest_laps["Difference"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))
    table = fastest_laps[["Driver", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time", "Difference", "Compound"]]
    table = table.replace("", "0")
    st.markdown("""
            <style>
            /* Center the table itself */
            .css-1d391kg {
                display: flex;
                justify-content: center;
            }
            /* Center the content of the table */
            table {
                margin: auto;
            }
            /* Center the content in the table cells */
            th, td {
                text-align: center !important;
            }
            </style>
            """, unsafe_allow_html=True)
    return table


def get_top_sectors(session):
    def add_color_cells(val):
        val = val.split(" ")[0]
        color = driver_colors[val]
        return f"background-color: {color}"

    drivers = pd.unique(session.laps["Driver"])
    fastest_laps = []
    for driver in drivers:
        fast_lap = session.laps.pick_driver(driver).pick_fastest()
        if not pd.isna(fast_lap["Driver"]):
            fastest_laps.append(fast_lap)

    driver_colors = {lap["Driver"]: fastf1.plotting.get_team_color(lap["Team"], session) for lap in fastest_laps}

    fastest_laps = Laps(fastest_laps)
    best_s1 = fastest_laps.sort_values(by="Sector1Time").reset_index(drop=True)[["Driver", "Sector1Time"]]
    best_s1["Sector1Time"] = best_s1["Sector1Time"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))

    best_s2 = fastest_laps.sort_values(by="Sector2Time").reset_index(drop=True)[["Driver", "Sector2Time"]]
    best_s2["Sector2Time"] = best_s2["Sector2Time"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))

    best_s3 = fastest_laps.sort_values(by="Sector3Time").reset_index(drop=True)[["Driver", "Sector3Time"]]
    best_s3["Sector3Time"] = best_s3["Sector3Time"].apply(lambda x: ":".join(str(x)[:-3].split(":")[2:]))

    lapTime = fastest_laps.sort_values(by="LapTime").reset_index(drop=True)[["Driver", "LapTime"]]
    lapTime["LapTime"] = lapTime["LapTime"].apply(lambda x: ":".join(str(x)[:-3].split(":")[1:]))

    best_s1 = best_s1["Driver"] + " " + best_s1["Sector1Time"]
    best_s2 = best_s2["Driver"] + " " + best_s2["Sector2Time"]
    best_s3 = best_s3["Driver"] + " " + best_s3["Sector3Time"]
    lapTime = lapTime["Driver"] + " " + lapTime["LapTime"]

    df = pd.DataFrame(columns=["Best Sector 1", "Best Sector 2", "Best Sector 3", "Lap Time"])
    df["Best Sector 1"] = best_s1
    df["Best Sector 2"] = best_s2
    df["Best Sector 3"] = best_s3
    df["Lap Time"] = lapTime

    df = df.style.map(add_color_cells)
    st.markdown(df.to_html(), unsafe_allow_html=True)


def get_driver_laps(session):

    drivers = pd.unique(session.laps["Driver"])

    selected_drivers = st.multiselect("Pick Driver", sorted(drivers))

    fig = go.Figure()
    for i, driver in enumerate(selected_drivers):
        driver_laps = session.laps.pick_driver(driver)
        laps = driver_laps.pick_quicklaps()
        laps = laps.reset_index(drop=True)
        laps["LapTime"] = laps["LapTime"].dt.total_seconds()
        laps["Compound"] = laps["Compound"].map({"SOFT": "red", "MEDIUM": "yellow", "HARD": "white",
                                                 "INTERMEDIATE": "green", "WET": "blue"})

        team = pd.unique(driver_laps["Team"])[0]
        team_color = fastf1.plotting.get_team_color(team, session)

        fig.add_trace(go.Violin(x=laps["Driver"], y=laps["LapTime"], meanline_visible=True,
                                line_color=team_color, showlegend=False))
        fig.add_trace(go.Scatter(x=laps["Driver"], y=laps["LapTime"], mode='markers',
                                 marker=dict(size=8, color=laps["Compound"]), showlegend=False))

    fig.add_trace(go.Scatter(
        x=[None],  # No actual data
        y=[None],
        mode='lines',
        name='SOFT',
        line=dict(color='red', width=5)  # Red line for SOFT
    ))

    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        name='MEDIUM',
        line=dict(color='yellow', width=5)  # Yellow line for MEDIUM
    ))

    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        name='HARD',
        line=dict(color='white', width=5)  # White line for HARD
    ))

    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        name='INTERMEDIATE',
        line=dict(color='green', width=5)  # Green line for INTERMEDIATE
    ))

    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        name='WET',
        line=dict(color='blue', width=5)  # Blue line for WET
    ))

    fig.update_layout(title="Laps Distribution", height=800, xaxis_title="Driver",
                      yaxis_title="Lap Time (seconds)")
    st.plotly_chart(fig)


def get_driver_tel(session):
    drivers = pd.unique(session.laps["Driver"])

    selected_drivers = st.multiselect("Pick Driver Tel", sorted(drivers))

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=False,
                        subplot_titles=("Telemetry", "RPM"))
    colors_used = set()
    for driver in selected_drivers:
        driver_laps = session.laps.pick_driver(driver)
        fast_lap = driver_laps.pick_fastest().get_car_data().add_distance()
        team = pd.unique(driver_laps["Team"])[0]
        team_color = fastf1.plotting.get_team_color(team, session)
        used = False
        if team_color in colors_used:
            used = True
        colors_used.add(team_color)

        fig.add_trace(go.Scatter(x=fast_lap["Distance"], y=fast_lap["Speed"],
                                 mode='lines', hovertemplate=driver + ' %{y}<extra></extra>',
                                 name=driver, line=dict(color=team_color, dash="dash" if used else "solid")),
                      row=1, col=1)

        fig.add_trace(go.Scatter(x=fast_lap["Distance"], y=fast_lap["RPM"],
                                 mode='lines', hovertemplate=driver + ' %{y}<extra></extra>',
                                 line=dict(color=team_color, dash="dash" if used else "solid"),
                                 showlegend=False), row=2, col=1)

    fig.update_layout(height=800, title="Driver Comparison", xaxis_title="Distance",
                      yaxis_title="Speed", hovermode="x unified")

    st.plotly_chart(fig)