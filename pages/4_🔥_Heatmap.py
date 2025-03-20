import streamlit as st
import leafmap.foliumap as leafmap
import requests

st.set_page_config(layout="wide")

st.sidebar.title("About")
st.sidebar.info("This is a Dengue Risk Heatmap for Lahore.")

st.title("Dengue Risk Heatmap")

# Load your CSV data from Google Colab or GitHub
url = "https://raw.githubusercontent.com/QamarAyesha/test-data/refs/heads/main/lahore_dengue_data.csv"  # If you uploaded it to Colab
response = requests.get(url)

if response.status_code == 200:
    print("URL is accessible")
else:
    print(f"Error: {response.status_code}")
df = pd.read_csv(url)

# Sidebar filter
risk_type = st.sidebar.selectbox("Select Risk Type",
                                  ["Weather_Risk_Score",
                                   "Water_Coverage_Risk_Score",
                                   "Past_Cases_Risk_Score",
                                   "Total_Risk_Score"])

# Create Map
m = leafmap.Map(center=[31.5204, 74.3587], zoom=12)
m.add_heatmap(
    data=df,
    latitude="Latitude",
    longitude="Longitude",
    value=risk_type,
    name="Dengue Risk Heatmap",
    radius=20,
)

m.to_streamlit(height=700)


