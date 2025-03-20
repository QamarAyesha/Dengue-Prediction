import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests

st.set_page_config(layout="wide")

st.sidebar.title("About")
st.sidebar.info("This is a Dengue Risk Heatmap for Lahore.")

st.title("Dengue Risk Heatmap")

# Load your CSV data from GitHub
url = "https://raw.githubusercontent.com/QamarAyesha/test-data/refs/heads/main/lahore_dengue_data.csv"
response = requests.get(url)

if response.status_code == 200:
    try:
        df = pd.read_csv(url)
        st.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()
else:
    st.error("Error loading data. Please check the URL.")
    st.stop()

# Sidebar filter
risk_type = st.sidebar.selectbox(
    "Select Risk Type",
    ["Weather_Risk_Score", "Water_Coverage_Risk_Score", "Past_Cases_Risk_Score", "Total_Risk_Score"]
)

# Validate columns
required_columns = ['Latitude', 'Longitude', risk_type]
if not all(col in df.columns for col in required_columns):
    st.error("Missing required columns in data.")
    st.stop()

# Handle missing or non-numeric data
if df[required_columns].isnull().any().any():
    st.warning("Data contains missing values. Removing rows with missing data.")
    df = df.dropna(subset=required_columns)

if not pd.api.types.is_numeric_dtype(df['Latitude']) or not pd.api.types.is_numeric_dtype(df['Longitude']):
    st.error("Latitude or Longitude columns contain non-numeric values.")
    st.stop()

if not pd.api.types.is_numeric_dtype(df[risk_type]):
    st.error(f"{risk_type} column contains non-numeric values.")
    st.stop()

# Create Map
m = leafmap.Map(center=[31.5204, 74.3587], zoom=12)

# Custom Gradient for Cooler Tones
gradient = {
    0.2: "rgba(0, 128, 255, 0.8)",
    0.4: "rgba(0, 204, 255, 0.8)",
    0.6: "rgba(102, 0, 204, 0.8)",
    0.8: "rgba(51, 51, 153, 0.8)",
    1.0: "rgba(0, 0, 102, 0.8)"
}

m.add_heatmap(
    data=df,
    latitude="Latitude",
    longitude="Longitude",
    value=risk_type,
    name="Dengue Risk Heatmap",
    radius=20,
    gradient=gradient

m.to_streamlit(height=700)



