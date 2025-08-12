import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Synthetic Energy Data & Privacy", page_icon="🔒", layout="wide")

st.title("🔒 Privacy-Preserving Synthetic Energy Dataset")
st.caption("Generate synthetic data, compare utility, and assess privacy risk (k-anonymity)")

np.random.seed(42)
real = pd.DataFrame({
    "household_id": range(1, 51),
    "day": np.random.randint(1, 8, 50),
    "total_kWh": np.round(np.random.normal(12, 3, 50).clip(3, 25), 2),
    "weekday": np.random.choice(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], 50),
    "tariff_type": np.random.choice(["Flat","TOU","CPP"], 50, p=[0.5, 0.35, 0.15]),
    "occupants": np.random.choice([1,2,3,4,5], 50, p=[0.15,0.35,0.3,0.15,0.05]),
    "home_type": np.random.choice(["Apt","Detached","Semi"], 50, p=[0.4,0.4,0.2])
})

st.sidebar.header("Controls")
n_syn = st.sidebar.slider("Synthetic rows", 50, 500, 150, 25)

# Fix: Use unique values and matching probabilities for tariff_type
unique_tariffs = real["tariff_type"].value_counts().index.tolist()
tariff_probs = real["tariff_type"].value_counts(normalize=True).values

syn = pd.DataFrame({
    "day": np.random.choice(real["day"], n_syn),
    "total_kWh": np.random.choice(real["total_kWh"], n_syn),
    "weekday": np.random.choice(real["weekday"], n_syn),
    "tariff_type": np.random.choice(unique_tariffs, n_syn, p=tariff_probs),
    "occupants": np.random.choice(real["occupants"], n_syn),
    "home_type": np.random.choice(real["home_type"], n_syn),
})

st.subheader("Utility Checks")
c1, c2 = st.columns(2)
with c1:
    st.markdown("Real tariff distribution")
    st.bar_chart(real["tariff_type"].value_counts(normalize=True))
with c2:
    st.markdown("Synthetic tariff distribution")
    st.bar_chart(syn["tariff_type"].value_counts(normalize=True))

st.markdown("Distribution of total_kWh")
hist = pd.DataFrame({"real": real["total_kWh"], "synthetic": syn["total_kWh"]})
fig = px.histogram(hist.melt(var_name="dataset", value_name="total_kWh"), x="total_kWh", color="dataset", barmode="overlay")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Privacy Risk: k-Anonymity")
qi = ["home_type","occupants","tariff_type"]
k_real = real.groupby(qi).size().min()
k_syn = syn.groupby(qi).size().min()
st.write(f"k-anonymity (real): {k_real}, (synthetic): {k_syn}")

st.markdown("Improve anonymity by bucketing occupants")
syn["occupants_bucket"] = pd.cut(syn["occupants"], bins=[0,2,4,100], labels=["1-2","3-4","5+"])
k_syn_bucketed = syn.groupby(["home_type","occupants_bucket","tariff_type"]).size().min()
st.write(f"k-anonymity after bucketing: {k_syn_bucketed}")

st.subheader("Download")
st.dataframe(syn.head())
st.caption("You can use Streamlit's download button extension or save the DataFrame locally when deploying the app.")