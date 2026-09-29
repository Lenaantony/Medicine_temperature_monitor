import streamlit as st

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
temperature = 9.2

# Temporary test storage range
MIN_TEMP = 2.0
MAX_TEMP = 8.0

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

temperatures = [2.1, 2.2, 2.3, 2.4, 4.2, 1.5]

st.line_chart(temperatures)

# Calculate statistics
minimum = min(temperatures)
maximum = max(temperatures)
average = sum(temperatures) / len(temperatures)

# Statistics
st.subheader("Temperature Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Minimum", f"{minimum:.2f} °C")

with col2:
    st.metric("Maximum", f"{maximum:.2f} °C")

with col3:
    st.metric("Average", f"{average:.2f} °C")