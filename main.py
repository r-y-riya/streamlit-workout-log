import streamlit as st
import pandas as pd
from data import get_exercise_data, add_exercise

# Title of the app
st.title("Workout Logger")

# Form to log a new exercise
with st.form("log_exercise"):
    exercise = st.text_input("Exercise")
    reps = st.number_input("Reps", min_value=1)
    sets = st.number_input("Sets", min_value=1)
    submit = st.form_submit_button("Log Exercise")

    if submit:
        add_exercise(exercise, reps, sets)
        st.success("Exercise logged!")

# Display the logged exercises
st.subheader("Logged Exercises")
data = get_exercise_data()
st.dataframe(data)
