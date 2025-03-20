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

# Ensure columns exist and are numeric
for col in required_columns:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()
    if not pd.api.types.is_numeric_dtype(df[col]):
        st.error(f"Column '{col}' must be numeric.")
        st.stop()

# Handle missing data
if df[required_columns].isnull().any().any():
    st.warning("Data contains missing values. Removing rows with missing data.")
    df = df.dropna(subset=required_columns)

# Normalize the risk scores
df[risk_type] = (df[risk_type] - df[risk_type].min()) / (df[risk_type].max() - df[risk_type].min())

# Define thresholds for risk levels
risk_thresholds = {
    'Low': 0.33,
    'Medium': 0.66,
    'High': 1.0
}

# Categorize risk_score into risk_level
df['risk_level'] = pd.cut(
    df[risk_type],
    bins=[0, risk_thresholds['Low'], risk_thresholds['Medium'], risk_thresholds['High']],
    labels=['Low', 'Medium', 'High']
)

# Map risk_level to numeric values for gradient
risk_level_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
df['risk_level_numeric'] = df['risk_level'].map(risk_level_mapping).astype(float)  # Convert to float

# Normalize risk_level_numeric to [0, 1] for gradient
df['risk_level_numeric'] = df['risk_level_numeric'] / 2

# Debug: Check risk_level_numeric values
st.write("Risk Level Numeric Values:")
st.write(df['risk_level_numeric'].value_counts())

# Debug: Check gradient
gradient = {
    0.0: "green",   # Low risk
    0.5: "yellow",  # Medium risk
    1.0: "red"      # High risk
}
st.write("Gradient:")
st.write(gradient)

# Create Map
m = leafmap.Map(center=[31.5204, 74.3587], zoom=12)

try:
    m.add_heatmap(
        data=df[['Latitude', 'Longitude', 'risk_level_numeric']].rename(columns={'risk_level_numeric': 'value'}),
        latitude="Latitude",
        longitude="Longitude",
        value="value",
        name="Dengue Risk Heatmap",
        radius=25,  # Adjust radius
        blur=15,    # Adjust blur
        gradient=gradient
    )
    st.success("Heatmap added successfully!")
except Exception as e:
    st.error(f"Error adding heatmap: {e}")

# Display map
m.to_streamlit(height=700)




