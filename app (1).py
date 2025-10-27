import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("🦠 COVID-19 Data Dashboard")
st.markdown("This interactive dashboard visualizes COVID-19 trends using a sample dataset.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("covid_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
countries = st.sidebar.multiselect(
    "Select Countries",
    options=df["country"].unique(),
    default=["India", "United States"]
)

filtered_df = df[df["country"].isin(countries)]

# Latest data
latest = filtered_df.groupby("country").last().reset_index()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Total Cases (Latest)", f"{latest['total_cases'].sum():,.0f}")
col2.metric("💀 Total Deaths (Latest)", f"{latest['total_deaths'].sum():,.0f}")
col3.metric("📈 Countries Selected", len(countries))

# Visualizations
st.markdown("### 📅 Total Cases Over Time")
fig1 = px.line(filtered_df, x="date", y="total_cases", color="country", title="Total Cases Over Time")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### ⚰️ New Deaths Over Time")
fig2 = px.line(filtered_df, x="date", y="new_deaths", color="country", title="New Deaths Over Time")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 🌍 Total Cases vs Deaths")
fig3 = px.scatter(latest, x="total_cases", y="total_deaths", size="population", color="country",
                  hover_name="country", title="Total Cases vs Total Deaths")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown("📊 Data source: Synthetic COVID dataset created for demonstration.")
