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

# --- Maharashtra Consumption Profile ---
def generate_maharashtra_consumption_profile():
    np.random.seed(42)
    hours, consumption = [], []
    base = [
        0.4, 0.3, 0.2, 0.2, 0.3, 0.5,
        1.8, 2.4, 2.0, 1.2, 0.9, 0.8,
        1.1, 0.9, 0.8, 1.0, 1.3, 1.8,
        3.2, 4.1, 3.8, 2.8, 2.1, 1.5
    ]
    start = datetime(2024, 1, 1)
    for d in range(7):
        cur = start + timedelta(days=d)
        is_weekend = d >= 5
        for h in range(24):
            ts = cur + timedelta(hours=h)
            v = base[h]
            if is_weekend:
                if 6 <= h <= 11:
                    v *= 0.8
                if 10 <= h <= 15:
                    v *= 1.4
                if 18 <= h <= 22:
                    v *= 1.3
            summer_factor = 1.0
            if 12 <= h <= 18:
                summer_factor = 1.6
            elif h >= 22 or h <= 6:
                summer_factor = 1.2
            v *= summer_factor
            v = max(0.1, v * np.random.normal(1.0, 0.15))
            hours.append(ts)
            consumption.append(round(v, 2))
    df = pd.DataFrame({
        "timestamp": hours,
        "hour": [t.hour for t in hours],
        "day_of_week": [t.strftime("%A") for t in hours],
        "consumption_kWh": consumption
    })
    return df

def maharashtra_pricing_arrays():
    flat = np.full(24, 8.50)
    tou = np.array([
        6.80, 6.80, 6.80, 6.80, 6.80, 6.80,
        11.05, 11.05, 11.05, 11.05,
        6.80, 6.80, 6.80, 6.80, 6.80, 6.80, 6.80, 6.80,
        11.05, 11.05, 11.05, 11.05,
        6.80, 6.80
    ])
    cpp = tou.copy()
    for h in [18, 19, 20]:
        cpp[h] = 28.0
    return flat, tou, cpp

def bill_calculator(df, rates24):
    r = pd.Series(rates24, index=range(24))
    return (df["consumption_kWh"] * r[df["hour"]].values).sum()

def maharashtra_nudge_algorithm(df, rates24, threshold=15.0, flex_pct=0.25):
    r = pd.Series(rates24, index=range(24))
    x = df.copy()
    x["rate"] = r[x["hour"]].values
    x["flex"] = x["consumption_kWh"] * flex_pct
    x["ess"] = x["consumption_kWh"] - x["flex"]
    out = []
    total_shifted = 0.0
    for day, g in x.groupby(x["timestamp"].dt.date):
        high = g[g["rate"] >= threshold].copy()
        low = g[g["rate"] < threshold].copy().sort_values("rate")
        shifted = g["flex"].values.copy()
        if len(high) and len(low):
            total_to_shift = high["flex"].sum()
            for idx in high.index:
                shifted[g.index.get_loc(idx)] = 0
            remaining = total_to_shift
            for idx in low.index:
                if remaining <= 0:
                    break
                loc = g.index.get_loc(idx)
                move = min(remaining, total_to_shift * 0.4)
                shifted[loc] += move
                remaining -= move
                total_shifted += move
        g["flex_shifted"] = shifted
        g["total_shifted"] = g["ess"] + g["flex_shifted"]
        out.append(g)
    res = pd.concat(out)
    base_cost = (res["consumption_kWh"] * res["rate"]).sum()
    new_cost = (res["total_shifted"] * res["rate"]).sum()
    return res, base_cost, new_cost, base_cost - new_cost, total_shifted

# --- Maharashtra App Section ---
st.title("⚡ Maharashtra Dynamic Tariff Explorer")
st.caption("Real MSEDCL tariffs and Maharashtra household consumption patterns")

df_maha = generate_maharashtra_consumption_profile()
flat_maha, tou_maha, cpp_maha = maharashtra_pricing_arrays()

st.sidebar.header("MSEDCL Tariff Controls")
scheme_maha = st.sidebar.selectbox(
    "Pricing Scheme (Maharashtra)", 
    ["Flat Rate (Current)", "Time-of-Use (2025+)", "Critical Peak Pricing"], 
    index=2
)

threshold_maha = st.sidebar.slider(
    "Nudge threshold (₹/kWh)", 
    5.0, 30.0, 15.0, 0.5,
    help="Price above which households shift flexible loads"
)

flex_pct_maha = st.sidebar.slider(
    "Flexible load (%) (Maharashtra)", 
    0, 50, 25, 5,
    help="Percentage of consumption that can be time-shifted"
)

st.sidebar.markdown("### Maharashtra Context")
st.sidebar.info("""
**MSEDCL Tariff Structure:**
- Residential: ₹4.71-16.64/unit
- Fixed charge: ₹128/month (1-phase)
- ToD implementation: April 2025
- Solar hours discount: 20%
""")

rates_maha = {"Flat Rate (Current)": flat_maha, "Time-of-Use (2025+)": tou_maha, "Critical Peak Pricing": cpp_maha}[scheme_maha]

b_flat_maha = bill_calculator(df_maha, flat_maha)
b_tou_maha = bill_calculator(df_maha, tou_maha)
b_cpp_maha = bill_calculator(df_maha, cpp_maha)

st.subheader("Weekly Bill Comparison (Maharashtra Household)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Flat Rate", f"₹{b_flat_maha:.2f}", "Current MSEDCL")
with col2:
    st.metric("Time-of-Use", f"₹{b_tou_maha:.2f}", f"₹{b_tou_maha-b_flat_maha:+.2f} vs Flat")
with col3:
    st.metric("Critical Peak", f"₹{b_cpp_maha:.2f}", f"₹{b_cpp_maha-b_flat_maha:+.2f} vs Flat")

res_maha, base_cost_maha, new_cost_maha, savings_maha, shifted_maha = maharashtra_nudge_algorithm(
    df_maha, rates_maha, threshold_maha, flex_pct_maha/100
)

st.subheader("Demand Response Impact")
st.write(f"""
**Original bill:** ₹{base_cost_maha:.2f} | **After load shifting:** ₹{new_cost_maha:.2f} | 
**Savings:** ₹{savings_maha:.2f} ({savings_maha/base_cost_maha*100:.1f}%) | **Energy shifted:** {shifted_maha:.1f} kWh
""")

st.subheader("Maharashtra Household Consumption (Original vs Optimized)")
fig_maha = make_subplots(
    rows=2, cols=1, 
    shared_xaxes=True, 
    subplot_titles=("Original Consumption Pattern", "After Demand Response")
)
fig_maha.add_trace(
    go.Scatter(
        x=df_maha["timestamp"], 
        y=df_maha["consumption_kWh"], 
        name="Original", 
        line=dict(color="blue")
    ), 
    1, 1
)
fig_maha.add_trace(
    go.Scatter(
        x=res_maha["timestamp"], 
        y=res_maha["total_shifted"], 
        name="Optimized", 
        line=dict(color="green")
    ), 
    2, 1
)
fig_maha.update_layout(height=500, yaxis_title="Consumption (kWh)", yaxis2_title="Consumption (kWh)")
st.plotly_chart(fig_maha, use_container_width=True)

st.subheader("MSEDCL Tariff Structure by Hour")
p_maha = pd.DataFrame({
    "hour": range(24), 
    "flat": flat_maha, 
    "tou": tou_maha, 
    "cpp": cpp_maha
})
pfig_maha = go.Figure()
pfig_maha.add_trace(go.Scatter(x=p_maha["hour"], y=p_maha["flat"], name="Flat Rate", mode="lines+markers"))
pfig_maha.add_trace(go.Scatter(x=p_maha["hour"], y=p_maha["tou"], name="Time-of-Use", mode="lines+markers"))
pfig_maha.add_trace(go.Scatter(x=p_maha["hour"], y=p_maha["cpp"], name="Critical Peak", mode="lines+markers"))
pfig_maha.update_layout(
    xaxis_title="Hour of Day", 
    yaxis_title="₹/kWh", 
    height=350,
    title="MSEDCL Pricing Schemes"
)
st.plotly_chart(pfig_maha, use_container_width=True)

st.subheader("Maharashtra Energy Insights")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Peak Consumption Patterns:**
    - Morning: 6-9 AM (tea, breakfast)
    - Evening: 6-9 PM (cooking, lighting)
    - Summer AC: 12-6 PM peak load
    """)
with col2:
    st.markdown("""
    **MSEDCL Tariff Benefits:**
    - Solar hours: 20% discount (10 AM-6 PM)
    - Off-peak: 6.80 ₹/kWh (night hours)
    - Peak penalty: Up to 28 ₹/kWh (6-9 PM)
    """)

if savings_maha > 0:
    annual_savings_maha = savings_maha * 52
    st.success(f"""
    **Annual Impact for Maharashtra Household:**
    - Weekly savings: ₹{savings_maha:.2f}
    - Annual savings: ₹{annual_savings_maha:.2f}
    - Peak load reduction: {shifted_maha:.1f} kWh/week
    """)
else:
    st.warning("Current constraints don't allow for bill savings. Try adjusting the flexible load percentage or nudge threshold.")
