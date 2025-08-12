import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Carbon-Intensity Scheduler", page_icon="🌱", layout="wide")

st.title("🌱 Carbon-Intensity–Aware Task Scheduler")
st.caption("Find the cleanest time window to run a flexible task")

hours = np.arange(24)
intensity = np.array([
    420,400,380,360,350,340,360,420,480,520,500,460,
    430,410,390,370,360,420,480,520,500,460,430,410
])
df = pd.DataFrame({"hour": hours, "carbon_intensity": intensity})

st.sidebar.header("Task Parameters")
duration = st.sidebar.slider("Task duration (hours)", 1, 6, 2, 1)
start_allowed = st.sidebar.slider("Earliest start", 0, 23, 8, 1)
end_allowed = st.sidebar.slider("Latest end (inclusive)", 1, 24, 23, 1)

# Compute best window
best_avg = float("inf")
best_start = None
for start in range(start_allowed, end_allowed - duration + 1):
    window = df.loc[df["hour"].between(start, start+duration-1), "carbon_intensity"]
    avg = window.mean()
    if avg < best_avg:
        best_avg = avg
        best_start = start

st.subheader("Recommended Window")
if best_start is not None:
    st.write(f"Best: {best_start}:00–{best_start+duration}:00 | Avg intensity: {best_avg:.0f} gCO2/kWh")
else:
    st.error("No feasible window given your constraints. Adjust sliders.")

st.subheader("Intensity Timeline")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["hour"], y=df["carbon_intensity"], mode="lines+markers", name="Carbon Intensity"))
if best_start is not None:
    sel = (df["hour"]>=best_start) & (df["hour"]<best_start+duration)
    fig.add_trace(go.Scatter(x=df.loc[sel,"hour"], y=df.loc[sel,"carbon_intensity"], mode="markers", marker=dict(size=12,color="green"), name="Recommended"))
fig.update_layout(xaxis_title="Hour", yaxis_title="gCO2/kWh", height=400)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Compare with Running Now")
run_now = st.sidebar.slider("Assume 'now' is (hour)", 0, 23, 9, 1)
now_avg = df.loc[df["hour"].between(run_now, min(23, run_now+duration-1)), "carbon_intensity"].mean()
if best_start is not None:
    savings = now_avg - best_avg
    st.write(f"If you run now ({run_now}:00), avg intensity is {now_avg:.0f}. Savings vs best slot: {savings:.0f} gCO2/kWh")
else:
    st.info("Set a feasible window to compare savings.")