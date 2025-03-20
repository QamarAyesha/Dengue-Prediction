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

# Ensure





