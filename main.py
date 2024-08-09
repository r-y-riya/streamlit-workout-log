# -*- coding: utf-8 -*-

import streamlit as st
import json
from datetime import datetime
import pandas as pd

# Function to map exercise names to video URLs
def get_video_url(exercise_name):
    # This is a placeholder. You should replace this with actual video URLs.
    return f"https://www.youtube.com/watch?v=placeholder_{exercise_name}"

# Function to format date
def format_date(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%B %d, %Y")


@st.cache_data
def load_exercises_from_json():
    with open("exercises.json", "r") as file:
        data = json.load(file)
    return data["exercises"]


# Main app
st.title("Rastreador de Treinos")

exercises_data = load_exercises_from_json()

# Create a dictionary to group exercises by category
exercises_by_category = {}
for exercise in exercises_data:
    category = exercise["category"]
    if category not in exercises_by_category:
        exercises_by_category[category] = []
    exercises_by_category[category].append(exercise)

# Create a Workout section
with st.expander("Criar um treino", expanded=not st.session_state.get('workout_created', False)):
    workout_name = st.text_input("Nome do treino")
    number_of_exercises = st.number_input(
        "Número de exercicios (1-6)", min_value=1, max_value=6, value=1
    )
    workout_notes = st.text_area("Observacoes do treino (opcional)")

    exercises = []

    for i in range(number_of_exercises):
        st.subheader(f"Exercicio {i+1}")

        col1, col2 = st.columns(2)

        with col1:
            categoria = st.selectbox(
                f"Selecione a Categoria {i+1}",
                options=list(exercises_by_category.keys()),
                key=f"cat_{i}",
            )

        with col2:
            selected_exercise = st.selectbox(
                f"Selecione o Exercicio {i+1}",
                options=[
                    f"{ex['exercise_name_ptbr']} | {ex['exercise_name_en']}"
                    for ex in exercises_by_category[categoria]
                ],
                key=f"ex_{i}",
            )

        selected_exercise_data = next(
            ex
            for ex in exercises_by_category[categoria]
            if f"{ex['exercise_name_ptbr']} | {ex['exercise_name_en']}" == selected_exercise
        )

        st.markdown(
            f"[{selected_exercise_data['exercise_name_ptbr']}]({selected_exercise_data['youtube_link']})"
        )
        st.write(selected_exercise_data["exercise_name_en"])

        col3, col4, col5 = st.columns(3)

        with col3:
            sets = st.number_input(
                f"Número de Series {i+1}", min_value=1, value=1, key=f"sets_{i}"
            )

        with col4:
            reps = st.number_input(
                f"Número de Repeticoes {i+1}", min_value=1, value=1, key=f"reps_{i}"
            )

        with col5:
            weight = st.number_input(
                f"Peso (kg) {i+1}", min_value=0.0, value=0.0, step=0.5, key=f"weight_{i}"
            )

        exercises.append(
            {
                "categoria": categoria,
                "exercicio": selected_exercise_data["exercise_name_ptbr"],
                "exercicio_en": selected_exercise_data["exercise_name_en"],
                "youtube_link": selected_exercise_data["youtube_link"],
                "series": sets,
                "repeticoes": reps,
                "peso": weight,
            }
        )

    if st.button("Criar Treino"):
        workout = {
            "nome": workout_name,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observacoes": workout_notes,
            "exercicios": exercises,
        }
        st.session_state.setdefault("treinos", []).append(workout)
        st.session_state['workout_created'] = True
        st.success(f"Treino '{workout_name}' criado com sucesso!")

st.header("Treino de Hoje")
if "treinos" in st.session_state and st.session_state.treinos:
    treino_hoje = st.session_state.treinos[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Data do Treino")
        st.write(format_date(treino_hoje['data']))
    
    with col2:
        st.subheader("Dicas")
        st.write("Dicas para seu treino aparecerão aqui. Mantenha-se hidratado e concentre-se na forma correta dos exercícios.")
    
    with col3:
        st.subheader("Sets e Reps")
        for exercicio in treino_hoje["exercicios"]:
            st.subheader(exercicio['exercicio'])
            col1, col2, col3 = st.columns(3)
            col1.metric("Sets", exercicio['series'])
            col2.metric("Reps", exercicio['repeticoes'])
            col3.metric("Peso (kg)", exercicio['peso'])
    
    with col4:
        st.subheader("Vídeo do Exercício")
        selected_exercise = st.selectbox("Selecione um exercício", 
                                         [ex['exercicio'] for ex in treino_hoje["exercicios"]])
        video_url = get_video_url(selected_exercise)
        st.video(video_url)

else:
    st.write("Ainda nao ha treino registrado hoje. Crie um novo treino!")
