import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from langchain_groq import ChatGroq

# Initialize ChatGroq
llm = ChatGroq(
    api_key="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",
    model="mixtral-8x7b-32768",
    temperature=0.7,
    max_tokens=1000,
    max_retries=2
)

# Function to parse input with ChatGroq
def parse_input_with_groq(user_input):
    messages = [
        ("system", "You are a helpful assistant for IoT data simulation."),
        ("human", user_input)
    ]
    response = llm.invoke(messages)
    return response.content  # Assuming response contains parsed data

# Data Generation Function
def generate_time_series(metrics, start_time, end_time, interval_minutes):
    timestamps = pd.date_range(start=start_time, end=end_time, freq=f"{interval_minutes}T")
    data = {"Timestamp": timestamps}
    for metric in metrics:
        if metric == "temperature":
            data[metric] = np.linspace(50, 100, len(timestamps))
        elif metric == "RPM":
            data[metric] = np.sin(np.linspace(0, 2 * np.pi, len(timestamps))) * 1000 + 2000
        else:
            data[metric] = np.random.uniform(10, 100, len(timestamps))
    return pd.DataFrame(data)

# Streamlit App
st.title("IoT Data Simulation with ChatGroq")

# Step 1: User Input
user_input = st.text_input("Describe the data you want to simulate:", 
                           "Generate time-series data for engine metrics like temperature, RPM, and torque.")

if st.button("Submit"):
    groq_response = parse_input_with_groq(user_input)
    st.write("ChatGroq Response:", groq_response)
    
    # Mock parsing the response for metrics
    metrics = ["temperature", "RPM"]  # Update based on actual response parsing
    st.subheader("Select Metrics")
    selected_metrics = st.multiselect("Choose metrics:", metrics, default=metrics)
    
    if selected_metrics:
        st.subheader("Configure Time-Series Data")
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", datetime.now().date())
        end_date = col2.date_input("End Date", (datetime.now() + timedelta(days=1)).date())
        interval_minutes = st.slider("Interval (minutes):", min_value=1, max_value=60, value=5)
        
        data = generate_time_series(selected_metrics, start_date, end_date, interval_minutes)
        st.subheader("Generated Data")
        st.dataframe(data)
        
        csv = data.to_csv(index=False)
        st.download_button("Download Data", csv, "simulated_data.csv", "text/csv")
