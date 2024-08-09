import streamlit as st
import pandas as pd
from datetime import datetime


@st.cache_data
def load_categorized_exercises():
    categorias = {}
    categoria_atual = ""
    with open("categorized_exercises.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                categoria_atual = line[:-1]
                categorias[categoria_atual] = []
            elif line.startswith("- "):
                categorias[categoria_atual].append(line[2:])
    return categorias


@st.cache_data
def load_exercises():
    df = pd.read_csv("exercises.csv")
    categorizados = load_categorized_exercises()

    # Cria um dicionario para mapear exercicios para categorias
    exercicio_para_categoria = {}
    for categoria, exercicios in categorizados.items():
        for exercicio in exercicios:
            exercicio_para_categoria[exercicio] = categoria

    # Adiciona coluna de categoria ao DataFrame
    df["categoria"] = df["name"].map(exercicio_para_categoria)
    return df


# Main app
st.title("Rastreador de Treinos")

exercicios_categorizados = load_categorized_exercises()
df_exercicios = load_exercises()

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
            options=list(exercicios_categorizados.keys()),
            key=f"cat_{i}",
        )

    with col2:
        nome_exercicio = st.selectbox(
            f"Selecione o Exercicio {i+1}",
            options=exercicios_categorizados[categoria],
            key=f"ex_{i}",
        )

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
            "exercicio": nome_exercicio,
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
        st.subheader(
            f"Exercicio {i}: {exercicio['exercicio']} ({exercicio['categoria']})"
        )
        st.write(
            f"Series: {exercicio['series']}, Repeticoes: {exercicio['repeticoes']}, Peso: {exercicio['peso']} kg"
        )
        youtube_link = f"https://www.youtube.com/results?search_query={exercicio['exercicio'].replace(' ', '+')}"
        st.markdown(f"[Ver video do exercicio no YouTube]({youtube_link})")
else:
    st.write("Ainda nao ha treino registrado hoje. Crie um novo treino!")
