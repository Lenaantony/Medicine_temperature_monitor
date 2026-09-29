import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from config import MEDICINE_LIMITS

load_dotenv()

username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))
cluster = os.getenv("MONGO_CLUSTER")

mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/"

client = MongoClient(mongo_uri)

db = client["medicine_monitor"]
collection = db["temperature_readings"]


# Page configuration
st.set_page_config(
    page_title="Medicine Storage Monitor",
    page_icon="🌡️",
    layout="wide"
)

# Title
st.title("🌡️ Medicine Storage Monitor")

# Medicine selection
medicine = st.selectbox(
    "Medicine",
    ["Medicine A", "Medicine B", "Medicine C"]
)

# Temporary test temperature
latest_reading = collection.find_one(
    sort=[("timestamp", -1)]
)

if latest_reading:
    temperature = latest_reading["temperature"]
    medicine_from_db = latest_reading["medicine"]
else:
    temperature = 0
    medicine_from_db = "No data"

# Temporary test storage range
MIN_TEMP, MAX_TEMP = MEDICINE_LIMITS[medicine]

# Calculate status
if MIN_TEMP <= temperature <= MAX_TEMP:
    status = "SAFE"
    alert = "SAFE"
else:
    status = "UNSAFE"
    alert = "TEMPERATURE OUT OF RANGE"

# Current information
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Current Temperature",
        f"{temperature} °C"
    )

with col2:
    st.metric(
        "Storage Status",
        status
    )

# Alert
st.subheader("Alert")
st.success(alert)

# Temperature history
st.subheader("Temperature History")

readings = list(
    collection.find().sort("timestamp", 1)
)

data = {
    "Time": [reading["timestamp"] for reading in readings],
    "Temperature": [reading["temperature"] for reading in readings]
}

df = pd.DataFrame(data)

st.line_chart(
    df,
    x="Time",
    y="Temperature"
)

# Calculate statistics
minimum = df["Temperature"].min()
maximum = df["Temperature"].max()
average = df["Temperature"].mean()

# Statistics
st.subheader("Temperature Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Minimum", f"{minimum:.2f} °C")

with col2:
    st.metric("Maximum", f"{maximum:.2f} °C")

with col3:
    st.metric("Average", f"{average:.2f} °C")

st.subheader("Alert History")

unsafe_readings = df[df["Temperature"].apply(
    lambda temp: temp < MIN_TEMP or temp > MAX_TEMP
)]

if unsafe_readings.empty:
    st.success("No temperature alerts recorded.")
else:
    st.dataframe(
        unsafe_readings,
        width="stretch"
    )