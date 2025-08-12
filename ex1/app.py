import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

st.set_page_config(page_title="Dynamic Tariff Explorer", page_icon="⚡", layout="wide")

def generate_consumption_profile():
    np.random.seed(42)
    hours, consumption = [], []
    base = [0.8,0.7,0.6,0.6,0.7,1.2, 2.5,3.2,2.8,1.8,1.5,1.4, 1.6,1.4,1.3,1.5,1.8,2.2, 3.5,3.8,3.2,2.5,1.8,1.2]
    start = datetime(2024,1,1)
    for d in range(7):
        cur = start + timedelta(days=d)
        wknd = d>=5
        for h in range(24):
            ts = cur + timedelta(hours=h)
            v = base[h]
            if wknd:
                if 6<=h<=11: v*=0.7
                if 10<=h<=14: v*=1.3
                if 18<=h<=22: v*=1.2
            v = max(0.1, v*np.random.normal(1.0,0.12))
            hours.append(ts); consumption.append(round(v,2))
    df = pd.DataFrame({
        "timestamp": hours,
        "hour": [t.hour for t in hours],
        "day_of_week": [t.strftime("%A") for t in hours],
        "consumption_kWh": consumption
    })
    return df

def pricing_arrays():
    flat = np.full(24, 0.12)
    tou = np.array([0.08 if (h>=22 or h<6) else (0.18 if (6<=h<9 or 17<=h<22) else 0.12) for h in range(24)])
    cpp = tou.copy()
    for h in [17,18,19]: cpp[h] = 0.35
    return flat, tou, cpp

def bill(df, rates24):
    r = pd.Series(rates24, index=range(24))
    return (df["consumption_kWh"] * r[df["hour"]].values).sum()

def nudge(df, rates24, threshold=0.20, flex_pct=0.25):
    r = pd.Series(rates24, index=range(24))
    x = df.copy()
    x["rate"] = r[x["hour"]].values
    x["flex"] = x["consumption_kWh"]*flex_pct
    x["ess"] = x["consumption_kWh"]-x["flex"]
    out=[]; total_shifted=0.0
    for day, g in x.groupby(x["timestamp"].dt.date):
        high=g[g["rate"]>=threshold].copy()
        low =g[g["rate"]< threshold].copy().sort_values("rate")
        shifted=g["flex"].values.copy()
        if len(high) and len(low):
            total_to_shift=high["flex"].sum()
            for idx in high.index:
                shifted[g.index.get_loc(idx)]=0
            rem=total_to_shift
            for idx in low.index:
                if rem<=0: break
                loc=g.index.get_loc(idx)
                move=min(rem, total_to_shift*0.4)
                shifted[loc]+=move; rem-=move; total_shifted+=move
        g["flex_shifted"]=shifted
        g["total_shifted"]=g["ess"]+g["flex_shifted"]
        out.append(g)
    res=pd.concat(out)
    base_cost=(res["consumption_kWh"]*res["rate"]).sum()
    new_cost =(res["total_shifted"]*res["rate"]).sum()
    return res, base_cost, new_cost, base_cost-new_cost, total_shifted

st.title("⚡ Dynamic Tariff Explorer")
st.caption("Understand how pricing and nudges affect bills and behavior")

df = generate_consumption_profile()
flat, tou, cpp = pricing_arrays()

st.sidebar.header("Controls")
scheme = st.sidebar.selectbox("Pricing Scheme", ["Flat Rate","Time-of-Use","Critical Peak Pricing"], index=2)
threshold = st.sidebar.slider("Nudge threshold ($/kWh)", 0.05, 0.40, 0.20, 0.01)
flex_pct = st.sidebar.slider("Flexible load (%)", 0, 50, 25, 5)

rates = {"Flat Rate": flat, "Time-of-Use": tou, "Critical Peak Pricing": cpp}[scheme]

b_flat = bill(df, flat)
b_tou = bill(df, tou)
b_cpp = bill(df, cpp)

st.subheader("Weekly Bill Comparison")
st.write(f"Flat: ${b_flat:.2f} | TOU: ${b_tou:.2f} | CPP: ${b_cpp:.2f}")

res, base_cost, new_cost, savings, shifted = nudge(df, rates, threshold, flex_pct/100)

st.subheader("Behavioral Nudging Results")
st.write(f"Original bill: ${base_cost:.2f} | After nudging: ${new_cost:.2f} | Savings: ${savings:.2f} | Shifted: {shifted:.1f} kWh")

st.subheader("Consumption Pattern (Original vs After Behavior Change)")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Original","After Nudging"))
fig.add_trace(go.Scatter(x=df["timestamp"], y=df["consumption_kWh"], name="Original", line=dict(color="blue")), 1,1)
fig.add_trace(go.Scatter(x=res["timestamp"], y=res["total_shifted"], name="After", line=dict(color="green")), 2,1)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Pricing by Hour")
p = pd.DataFrame({"hour": range(24), "flat": flat, "tou": tou, "cpp": cpp})
pfig = go.Figure()
pfig.add_trace(go.Scatter(x=p["hour"], y=p["flat"], name="Flat", mode="lines+markers"))
pfig.add_trace(go.Scatter(x=p["hour"], y=p["tou"], name="TOU", mode="lines+markers"))
pfig.add_trace(go.Scatter(x=p["hour"], y=p["cpp"], name="CPP", mode="lines+markers"))
pfig.update_layout(xaxis_title="Hour", yaxis_title="$/kWh", height=350)
st.plotly_chart(pfig, use_container_width=True)

