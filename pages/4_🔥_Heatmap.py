import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
import requests
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
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

# Sidebar for selecting risk type
risk_type = st.sidebar.selectbox(
    "Select Risk Type",
    ["Weather_Risk_Score", "Water_Coverage_Risk_Score", "Past_Cases_Risk_Score", "Total_Risk_Score"]
)

# Validate columns
required_columns = ['Latitude', 'Longitude', risk_type]
if not all(col in df.columns for col in required_columns):
    st.error("Missing required columns in data.")
    st.stop()

# Clean data
if df[required_columns].isnull().any().any():
    st.warning("Data contains missing values. Removing rows with missing data.")
    df = df.dropna(subset=required_columns)

# Define a custom gradient for the heatmap
gradient = {
    0.2: "blue",
    0.4: "cyan",
    0.6: "lime",
    0.8: "yellow",
    1.0: "red"
}

# Create Folium Map
m = folium.Map(location=[31.5204, 74.3587], zoom_start=12)

# Add Heatmap Layer
heat_data = df[['Latitude', 'Longitude', risk_type]].values.tolist()
HeatMap(heat_data, radius=15, gradient=gradient).add_to(m)

# Display Map in Streamlit
st_folium(m, width=1200, height=700)  




