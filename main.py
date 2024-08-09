# -*- coding: utf-8 -*-

import streamlit as st
import json
from datetime import datetime
import pandas as pd


# Function to map exercise names to video URLs
def get_video_url(exercise_name):
    # This should be replaced with an actual video URL lookup or API call
    video_mapping = {
        "Squat": "https://www.youtube.com/watch?v=actual_squat_video",
        "Bench Press": "https://www.youtube.com/watch?v=actual_bench_press_video",
        "Deadlift": "https://www.youtube.com/watch?v=actual_deadlift_video",
        # Add more mappings as needed
    }
    return video_mapping.get(
        exercise_name, "https://www.youtube.com/watch?v=default_video"
    )


# Function to format date
def format_date(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%B %d, %Y")


@st.cache_data
def load_exercises_from_json():
    try:
        with open("exercises.json", "r") as file:
            data = json.load(file)
        return data["exercises"]
    except FileNotFoundError:
        st.error(
            "exercises.json file not found. Please make sure it exists in the same directory as this script."
        )
        return []
    except json.JSONDecodeError:
        st.error("exercises.json is not a valid JSON file. Please check its contents.")
        return []


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
with st.expander(
    "Criar um treino", expanded=not st.session_state.get("workout_created", False)
):
    workout_name = st.text_input("Nome do treino")
    number_of_exercises = st.number_input("Número de exercicios", min_value=1, value=1)
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
            exercise_options = [
                f"{ex['exercise_name_ptbr']} | {ex['exercise_name_en']}"
                for ex in exercises_by_category[categoria]
            ]
            selected_exercise = st.selectbox(
                f"Selecione o Exercicio {i+1}",
                options=exercise_options,
                key=f"ex_{i}",
            )

        selected_exercise_data = next(
            ex
            for ex in exercises_by_category[categoria]
            if f"{ex['exercise_name_ptbr']} | {ex['exercise_name_en']}"
            == selected_exercise
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
                f"Peso (kg) {i+1}",
                min_value=0.0,
                value=0.0,
                step=0.5,
                key=f"weight_{i}",
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
        st.session_state["workout_created"] = True
        st.success(f"Treino '{workout_name}' criado com sucesso!")

st.header("Treino de Hoje")
if "treinos" in st.session_state and st.session_state.treinos:
    treino_hoje = st.session_state.treinos[-1]

    col1, col2 = st.columns(2)

    with col1:
        # Workout Date card
        with st.container():
            st.write(format_date(treino_hoje["data"]))

        # Sets and Reps card
        with st.container():
            for exercicio in treino_hoje["exercicios"]:
                st.subheader(exercicio["exercicio"])
                col_sets, col_reps, col_weight = st.columns(3)
                with col_sets:
                    st.metric("Sets", exercicio["series"])
                with col_reps:
                    st.metric("Reps", exercicio["repeticoes"])
                with col_weight:
                    st.metric("Peso (kg)", exercicio["peso"])

    with col2:
        # Dicas card
        with st.container():
            st.write(
                "Dicas para seu treino aparecerão aqui. Mantenha-se hidratado e concentre-se na forma correta dos exercícios."
            )

        # Exercise Video card
        with st.container():
            st.subheader("Vídeo do Exercício")
            selected_exercise = st.selectbox(
                "Selecione um exercício",
                [ex["exercicio"] for ex in treino_hoje["exercicios"]],
            )
            video_url = get_video_url(selected_exercise)
            try:
                st.video(video_url)
            except Exception as e:
                st.error(f"Erro ao carregar o vídeo: {str(e)}")
                st.write("Por favor, tente novamente mais tarde ou contate o suporte.")

else:
    st.write("Ainda nao ha treino registrado hoje. Crie um novo treino!")
