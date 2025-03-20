import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests

st.set_page_config(layout="wide")

st.sidebar.title("About")
st.sidebar.info("This is a Dengue Risk Heatmap for Lahore.")

st.title("Dengue Risk Heatmap")

# Load your CSV data
url = "https://raw.githubusercontent.com/QamarAyesha/test-data/refs/heads/main/lahore_dengue_data.csv"
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(url)
    print("URL is accessible")
else:
    st.error(f"Error: {response.status_code}")

# Sidebar filter
risk_type = st.sidebar.selectbox("Select Risk Type",
                                  ["Weather_Risk_Score",
                                   "Water_Coverage_Risk_Score",
                                   "Past_Cases_Risk_Score",
                                   "Total_Risk_Score"])

# Gradient with Cooler Tones (Blue to Purple)
gradient = {
    0.2: "#B3E5FC",  # Light Blue
    0.4: "#4FC3F7",  # Teal Blue
    0.6: "#0288D1",  # Medium Blue
    0.8: "#6A1B9A"   # Purple
}

# Create Map
m = leafmap.Map(center=[31.5204, 74.3587], zoom=12)
m.add_heatmap(
    data=df,
    latitude="Latitude",
    longitude="Longitude",
    value=risk_type,
    name="Dengue Risk Heatmap",
    radius=20,
    gradient=gradient,
)

m.to_streamlit(height=700)

