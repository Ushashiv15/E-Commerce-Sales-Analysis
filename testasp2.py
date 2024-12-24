#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pickle
import pandas as pd
import streamlit as st

# Function to load the trained SARIMAX model
@st.cache_data
def load_sarimax_model():
    with open('sarimax_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Main app
st.title("Amazon Stock Price Prediction")

# Load the trained model
model = load_sarimax_model()

# Sidebar for user input
steps = st.sidebar.number_input(
    "Enter the number of days to predict:",
    min_value=1, max_value=365, value=30, step=1
)

# Forecasting function
def forecast_stock_price(steps):
    # Forecasting using the SARIMAX model
    forecast = model.get_forecast(steps=steps)
    forecast_values = forecast.predicted_mean
    forecast_conf_int = forecast.conf_int()

    # Create a DataFrame to display the forecast and its confidence intervals
    forecast_df = pd.DataFrame({
        'Date': pd.date_range(start='2024-11-21', periods=steps, freq='B'),  # Replace with actual start date
        'Forecasted_Price': forecast_values,
        'Lower_Bound': forecast_conf_int.iloc[:, 0],
        'Upper_Bound': forecast_conf_int.iloc[:, 1]
    })
    return forecast_df

# Get the forecast for the selected number of days
forecast_df = forecast_stock_price(steps)

# Display forecasted values and confidence intervals
st.write("### Forecasted Stock Prices")
st.write(forecast_df)

# Plot forecasted values
st.write("### Forecasted Stock Prices Visualization")
st.line_chart(forecast_df.set_index('Date'))



# In[ ]:




