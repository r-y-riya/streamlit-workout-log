import csv
from collections import defaultdict

# Define categories and keywords
categories = {
    "Full Body": ["burpee", "thruster", "turkish", "snatch", "clean", "jerk"],
    "Upper Body": ["push", "pull", "press", "bench", "shoulder", "chest", "tricep", "bicep", "curl", "row", "fly"],
    "Lower Body": ["squat", "lunge", "deadlift", "calf", "leg"],
    "Core": ["crunch", "plank", "ab", "situp", "v-up", "hollow", "russian twist"],
    "Cardio": ["run", "jump", "high knee", "mountain climber"],
    "Back": ["back", "lat", "pulldown", "row"],
    "Mobility/Flexibility": ["mobility", "stretch", "rotation"]
}

# Initialize defaultdict to store exercises by category
categorized_exercises = defaultdict(list)

# Read the CSV data
with open('exercises.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    exercises = list(csv_reader)

# Categorize exercises
for exercise in exercises:
    name = exercise[0].lower()
    categorized = False
    for category, keywords in categories.items():
        if any(keyword in name for keyword in keywords):
            categorized_exercises[category].append(exercise[0])
            categorized = True
            break
    if not categorized:
        categorized_exercises["Other"].append(exercise[0])

# Write categorized exercises to a file
with open('categorized_exercises.txt', 'w', encoding='utf-8') as outfile:
    for category, exercises in categorized_exercises.items():
        outfile.write(f"\n{category}:\n")
        for exercise in exercises:
            outfile.write(f"- {exercise}\n")

    outfile.write("\nNote: Some exercises may appear in multiple categories due to overlapping keywords.\n")

print("Categorization complete. Results have been saved to 'categorized_exercises.txt'.")