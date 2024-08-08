import pandas as pd

# Initialize an empty DataFrame to store exercise data
exercise_data = pd.DataFrame(columns=["Exercise", "Reps", "Sets"])

EXERCISES = [
    {"name": "Push-up", "video_link": "https://www.youtube.com/watch?v=_l3ySVKYVJ8"},
    {"name": "Squat", "video_link": "https://www.youtube.com/watch?v=aclHkVaku9U"},
    {"name": "Lunge", "video_link": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"},
    {"name": "Plank", "video_link": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
    {"name": "Burpee", "video_link": "https://www.youtube.com/watch?v=TU8QYVW0gDU"}
]
    return exercise_data

    def add_exercise(exercise, reps, sets):
        global exercise_data
        new_entry = {"Exercise": exercise, "Reps": reps, "Sets": sets}
        exercise_data = exercise_data.append(new_entry, ignore_index=True)
