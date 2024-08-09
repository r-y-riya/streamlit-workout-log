# List of Python Scripts

## categorize_exercises.py
```
import csv
from collections import defaultdict

# Define categories and keywords
categories = {
    "Full Body": ["burpee", "thruster", "turkish", "snatch", "clean", "jerk"],
    "Upper Body": [
        "push",
        "pull",
        "press",
        "bench",
        "shoulder",
        "chest",
        "tricep",
        "bicep",
        "curl",
        "row",
        "fly",
    ],
    "Lower Body": ["squat", "lunge", "deadlift", "calf", "leg"],
    "Core": ["crunch", "plank", "ab", "situp", "v-up", "hollow", "russian twist"],
    "Cardio": ["run", "jump", "high knee", "mountain climber"],
    "Back": ["back", "lat", "pulldown", "row"],
    "Mobility/Flexibility": ["mobility", "stretch", "rotation"],
}

# Initialize defaultdict to store exercises by category
categorized_exercises = defaultdict(list)

# Read the CSV data
with open("exercises.csv", "r", encoding="utf-8") as file:
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
with open("categorized_exercises.txt", "w", encoding="utf-8") as outfile:
    for category, exercises in categorized_exercises.items():
        outfile.write(f"\n{category}:\n")
        for exercise in exercises:
            outfile.write(f"- {exercise}\n")

    outfile.write(
        "\nNote: Some exercises may appear in multiple categories due to overlapping keywords.\n"
    )

print(
    "Categorization complete. Results have been saved to 'categorized_exercises.txt'."
)
```

## data.py
```
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
```

## generate_codebase.py
```
import os


def generate_md_file():
    md_filename = "codebase.md"
    with open(md_filename, "w") as md_file:
        md_file.write("# List of Python Scripts\n\n")
        for file in os.listdir("."):
            if file.endswith(".py"):
                md_file.write(f"## {file}\n")
                md_file.write("```\n")  # Start the code block
                with open(file, "r") as py_file:
                    md_file.write(py_file.read())
                md_file.write("```\n\n")  # End the code block


if __name__ == "__main__":
    generate_md_file()
```

## main.py
```
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

st.header("Registrar um Treino")

# Cria duas colunas para os menus suspensos
col1, col2 = st.columns(2)

with col1:
    categoria = st.selectbox("Selecione a Categoria", options=list(exercicios_categorizados.keys()))

with col2:
    nome_exercicio = st.selectbox("Selecione o Exercicio", options=exercicios_categorizados[categoria])

with st.form("workout_form"):
    col3, col4, col5 = st.columns(3)
    
    with col3:
        sets = st.number_input("Número de Series", min_value=1, value=1)
    
    with col4:
        reps = st.number_input("Número de Repeticoes", min_value=1, value=1)
    
    with col5:
        weight = st.number_input("Peso (kg)", min_value=0.0, value=0.0, step=0.5)
    
    notes = st.text_area("Observacoes (opcional)")
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
        st.success(f"Registrado: {nome_exercicio} ({categoria}), {sets} series, {reps} repeticoes, {weight} kg")

st.header("Histórico de Treinos")
if 'historico_treinos' in st.session_state and st.session_state.historico_treinos:
    df_historico = pd.DataFrame(st.session_state.historico_treinos)
    st.dataframe(df_historico)
else:
    st.write("Ainda nao ha histórico de treinos. Comece a registrar seus treinos!")
```

