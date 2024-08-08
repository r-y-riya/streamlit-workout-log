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

    # Cria um dicionário para mapear exercícios para categorias
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

st.header("Registrar um Treino")

# Cria duas colunas para os menus suspensos
col1, col2 = st.columns(2)

with col1:
    categoria = st.selectbox("Selecione a Categoria", options=list(exercicios_categorizados.keys()))

with col2:
    nome_exercicio = st.selectbox("Selecione o Exercício", options=exercicios_categorizados[categoria])

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
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categoria": categoria,
            "exercicio": nome_exercicio,
            "series": sets,
            "repeticoes": reps,
            "peso": weight,
            "observacoes": notes
        }
        st.session_state.setdefault('historico_treinos', []).append(registro)
        st.success(f"Registrado: {nome_exercicio} ({categoria}), {sets} séries, {reps} repetições, {weight} kg")

st.header("Histórico de Treinos")
if 'historico_treinos' in st.session_state and st.session_state.historico_treinos:
    df_historico = pd.DataFrame(st.session_state.historico_treinos)
    st.dataframe(df_historico)
else:
    st.write("Ainda não há histórico de treinos. Comece a registrar seus treinos!")
