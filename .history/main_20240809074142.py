import streamlit as st
import json
from datetime import datetime


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

st.header("Criar um treino")

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
    st.success(f"Treino '{workout_name}' criado com sucesso!")

st.header("Treino de Hoje")
if "treinos" in st.session_state and st.session_state.treinos:
    treino_hoje = st.session_state.treinos[-1]
    st.write(f"Nome: {treino_hoje['nome']}")
    st.write(f"Data: {treino_hoje['data']}")
    st.write(f"Observacoes: {treino_hoje['observacoes']}")

    for i, exercicio in enumerate(treino_hoje["exercicios"], 1):
        st.subheader(f"Exercicio {i}")
        st.markdown(
            f"{exercicio['categoria']} | [{exercicio['exercicio']}]({exercicio['youtube_link']})"
        )
        st.write(exercicio["exercicio_en"])
        st.write(
            f"Series: {exercicio['series']}, Repeticoes: {exercicio['repeticoes']}, Peso: {exercicio['peso']} kg"
        )
else:
    st.write("Ainda nao ha treino registrado hoje. Crie um novo treino!")
