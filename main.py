import streamlit as st
import pandas as pd
from data import get_exercise_data, add_exercise, EXERCISES

# Title of the app
st.title("Workout Logger")

# Section for viewing the exercise list
st.header("Exercise List")
st.write("Here are some exercises you can do along with video tutorials:")


def display_exercise_list():
    for exercise in EXERCISES:
        st.markdown(
            f"**{exercise['name']}**: [Video Tutorial]({exercise['video_link']})"
        )


display_exercise_list()

# Section for logging new workouts
st.header("Log a New Workout")
with st.form("log_exercise"):
    exercise = st.text_input("Exercise", placeholder="Enter the exercise name")
    reps = st.number_input("Reps", min_value=1, step=1)
    sets = st.number_input("Sets", min_value=1, step=1)
    submit = st.form_submit_button("Log Exercise")

    if submit:
        add_exercise(exercise, reps, sets)
        st.success("Exercise logged!")

# Section for displaying the workout history
st.header("Workout History")
st.write("Here is the history of your logged workouts:")
data = get_exercise_data()
st.dataframe(data)
import streamlit as st
import pandas as pd
import subprocess
from data import get_exercise_data, add_exercise

# Run the script to scrape exercises
subprocess.run(["python", "scrape_exercises.py"])

# Load exercises from CSV
exercises_df = pd.read_csv("exercises.csv")
EXERCISES = exercises_df.to_dict(orient="records")

def display_exercise_list():
    "Display exercises with video links"
    for exercise in EXERCISES:
        st.write(f"[{exercise['exercise']}]({exercise['url']})")

# Streamlit app
st.title("Workout Logger")
st.header("Exercise List")
display_exercise_list()

st.header("Log a New Workout")
with st.form("log_exercise"):
    exercise = st.text_input("Exercise")
    reps = st.number_input("Reps", min_value=1)
    sets = st.number_input("Sets", min_value=1)
    submitted = st.form_submit_button("Log Exercise")
    if submitted:
        add_exercise(exercise, reps, sets)
        st.success("Exercise logged!")

st.header("Workout History")
st.write(get_exercise_data())
