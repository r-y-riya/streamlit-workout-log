import streamlit as st
import pandas as pd
from datetime import datetime

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

# Main app
st.title("Rastreador de Treinos")

categorized_exercises = load_categorized_exercises()
exercises_df = load_exercises()

st.header("Registrar um Treino")

# Create two columns for the dropdowns
col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("Selecione a Categoria", options=list(categorized_exercises.keys()))

with col2:
    exercise_name = st.selectbox("Selecione o Exercício", options=categorized_exercises[category])

with st.form("workout_form"):
    col3, col4, col5 = st.columns(3)
    
    with col3:
        sets = st.number_input("Número de Séries", min_value=1, value=1)
    
    with col4:
        reps = st.number_input("Número de Repetições", min_value=1, value=1)
    
    with col5:
        weight = st.number_input("Peso (kg)", min_value=0.0, value=0.0, step=0.5)
    
    notes = st.text_area("Observações (opcional)")
    submit_button = st.form_submit_button("Registrar Treino")

    if submit_button:
        # Here you would typically save this to a database
        # For this example, we'll just display a success message
        log_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "exercise": exercise_name,
            "sets": sets,
            "reps": reps,
            "weight": weight,
            "notes": notes
        }
        st.session_state.setdefault('workout_history', []).append(log_entry)
        st.success(f"Registrado: {exercise_name} ({category}), {sets} séries, {reps} repetições, {weight} kg")

st.header("Histórico de Treinos")
if 'workout_history' in st.session_state and st.session_state.workout_history:
    history_df = pd.DataFrame(st.session_state.workout_history)
    st.dataframe(history_df)
else:
    st.write("Ainda não há histórico de treinos. Comece a registrar seus treinos!")
