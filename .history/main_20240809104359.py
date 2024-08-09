import streamlit as st
from datetime import datetime
import json

# Function to load exercises from JSON (placeholder)
def load_exercises_from_json():
    # This should be replaced with actual JSON loading logic
    return [{"exercise_name_ptbr": "Push Press", "exercise_name_en": "Push Press"}]

# Function to get video URL (placeholder)
def get_video_url(exercise_name):
    # This should be replaced with actual video URL lookup
    return "https://www.youtube.com/watch?v=default_video"

# Main app
st.title("Rastreador de Treinos")

# Create a 2x2 layout
col1, col2 = st.columns(2)

with col1:
    # Quadrant 1: Workout Summary
    st.subheader("Treino de Hoje")
    st.write(datetime.now().strftime("%B %d, %Y"))
    
    exercise = st.selectbox("Selecione o Exercício", ["Push Press"])
    
    col_sets, col_reps, col_weight = st.columns(3)
    with col_sets:
        sets = st.number_input("Sets", min_value=1, value=3)
    with col_reps:
        reps = st.number_input("Reps", min_value=1, value=10)
    with col_weight:
        weight = st.number_input("Peso (kg)", min_value=0.0, value=40.0, step=0.5)

with col2:
    # Quadrant 2: Exercise Video
    st.subheader("Vídeo do Exercício")
    selected_exercise = st.selectbox("Selecione um exercício para o vídeo", ["Push Press"])
    video_url = get_video_url(selected_exercise)
    st.video(video_url)

with col1:
    # Quadrant 3: Workout Tips
    st.subheader("Dicas de Treino")
    st.write("Mantenha-se hidratado e concentre-se na forma correta dos exercícios.")
    st.markdown("""
    - Respire regularmente durante os exercícios
    - Mantenha a postura correta
    - Faça aquecimento antes de começar
    """)

with col2:
    # Quadrant 4: Execução do Exercício
    st.subheader("Execução do Exercício")
    st.write(f"Exercício atual: {exercise}")
    
    completed_sets = st.empty()
    set_button = st.button("Marcar Set como Completo")
    
    if 'completed_sets' not in st.session_state:
        st.session_state.completed_sets = 0
    
    if set_button and st.session_state.completed_sets < sets:
        st.session_state.completed_sets += 1
    
    completed_sets.write(f"Sets completados: {st.session_state.completed_sets}/{sets}")
    
    if st.session_state.completed_sets == sets:
        st.success("Exercício Completo!")
    
    st.text_area("Notas:", placeholder="Adicione notas sobre sua execução...")

# Reset button
if st.button("Resetar Treino"):
    st.session_state.completed_sets = 0
    st.experimental_rerun()