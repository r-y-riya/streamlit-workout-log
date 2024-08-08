import pandas as pd

# Initialize an empty DataFrame to store exercise data
exercise_data = pd.DataFrame(columns=["Exercise", "Reps", "Sets"])


def get_exercise_data():
    return exercise_data


def add_exercise(exercise, reps, sets):
    global exercise_data
    new_entry = {"Exercise": exercise, "Reps": reps, "Sets": sets}
    exercise_data = pd.concat(
        [exercise_data, pd.DataFrame([new_entry])], ignore_index=True
    )
