import streamlit as st
import pandas as pd


@st.cache_data
def load_categorized_exercises():
    categories = {}
    current_category = ""
    with open("categorized_exercises.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                current_category = line[:-1]
                categories[current_category] = []
            elif line.startswith("- "):
                categories[current_category].append(line[2:])
    return categories


@st.cache_data
def load_exercises():
    df = pd.read_csv("exercises.csv")
    categorized = load_categorized_exercises()

    # Create a dictionary to map exercises to categories
    exercise_to_category = {}
    for category, exercises in categorized.items():
        for exercise in exercises:
            exercise_to_category[exercise] = category

    # Add category column to DataFrame
    df["category"] = df["name"].map(exercise_to_category)
    return df


def display_exercise_list(categorized_exercises):
    for category, exercises in categorized_exercises.items():
        with st.expander(f"{category} Exercises"):
            for exercise in exercises:
                st.write(f"- {exercise}")


# Main app
st.title("Workout Tracker")

categorized_exercises = load_categorized_exercises()
exercises_df = load_exercises()

st.header("Exercise List")
display_exercise_list(categorized_exercises)

st.header("Log a Workout")
with st.form("workout_form"):
    category = st.selectbox(
        "Select Category", options=list(categorized_exercises.keys())
    )
    exercise_name = st.selectbox(
        "Select Exercise", options=categorized_exercises[category]
    )
    sets = st.number_input("Number of Sets", min_value=1, value=1)
    reps = st.number_input("Number of Reps", min_value=1, value=1)
    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0, step=0.5)
    submit_button = st.form_submit_button("Log Workout")

    if submit_button:
        # Here you would typically save this to a database
        # For this example, we'll just display a success message
        st.success(
            f"Logged: {exercise_name} ({category}), {sets} sets, {reps} reps, {weight} kg"
        )

st.header("Workout History")
# Here you would typically load and display the workout history from a database
st.write("Your workout history will be displayed here.")
