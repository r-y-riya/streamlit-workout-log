import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime

# Run the scraping script
subprocess.run(["python", "scrape_exercises.py"])

# Load exercises from CSV
@st.cache_data
def load_exercises():
    return pd.read_csv('exercises.csv')

exercises_df = load_exercises()

def display_exercise_list():
    st.write("Available Exercises:")
    for _, exercise in exercises_df.iterrows():
        st.write(f"- [{exercise['name']}]({exercise['link']})")

st.title("Workout Tracker")

st.header("Exercise List")
display_exercise_list()

st.header("Log a Workout")
with st.form("workout_form"):
    exercise_name = st.selectbox("Select Exercise", options=exercises_df['name'].tolist())
    sets = st.number_input("Number of Sets", min_value=1, value=1)
    reps = st.number_input("Number of Reps", min_value=1, value=1)
    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0, step=0.5)
    submit_button = st.form_submit_button("Log Workout")

    if submit_button:
        # Here you would typically save this to a database
        # For this example, we'll just display a success message
        st.success(f"Logged: {exercise_name}, {sets} sets, {reps} reps, {weight} kg")

st.header("Workout History")
# Here you would typically load and display the workout history from a database
st.write("Your workout history will be displayed here.")