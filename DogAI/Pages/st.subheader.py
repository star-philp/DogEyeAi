import streamlit as st  # Import the Streamlit library
import pandas as pd
import plotly.express as px
from db_handler import load_data  # Ensure this import is correct

# Display saved results from the database
st.subheader("Previously Saved Results")
data = load_data()
if data is not None:
    st.dataframe(data)
    
    # Class Distribution Visualization
    st.subheader("Class Distribution")
    class_distribution = data['class'].value_counts().reset_index()
    class_distribution.columns = ['Class', 'Count']
    fig = px.bar(class_distribution, x='Class', y='Count', color='Class', title='Class Distribution')
    st.plotly_chart(fig)

    # Analysis Over Time Visualization
    st.subheader("Analysis Over Time")  # Correct subheader for time analysis
    data['analysis_time'] = pd.to_datetime(data['analysis_time'])
    time_series = data.set_index('analysis_time').resample('D').size().reset_index()
    time_series.columns = ['Date', 'Count']
    fig = px.line(time_series, x='Date', y='Count', title='Analysis Over Time')
    st.plotly_chart(fig)
else:
    st.write("No data available.")
