import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Simulador de Casos Clínicos", page_icon="🩺", layout="wide")
st.title("🩺 Simulador Clínico Interactivo")

# --- MODO DOCENTE (Configuración Dinámica) ---
# Usamos un 'expander' para que esta sección se pueda ocultar a los alumnos
with st.expander("⚙️ PANEL DOCENTE (Configurar Nuevo Caso)", expanded=False):
    st.markdown("Escribe aquí los detalles del paciente. Los alumnos no verán esta información.")
    
    nuevo_prompt = st.text_area(
        "1. Personalidad y Reglas de la IA (El Prompt):", 
        value="Eres Roberto, 65 años, carpintero. Tienes mareos y presíncope al usar el brazo izquierdo. No des tu diagnóstico. Responde corto.",
        height=150
    )
    
    nuevo_fisico = st.text_input(
        "2. Hallazgos al Examen Físico (Visible si el alumno lo pide):", 
        value="PA Brazo Derecho: 140/85 mmHg | Brazo Izquierdo: 95/60 mmHg"
    )
    
    nuevo_pocus = st.text_input(
        "3. Hallazgos POCUS (Visible si el alumno pide ecografía):", 
        value="Flujo retrógrado en arteria vertebral izquierda y curva tardus-parvus en braquial."
    )
    
    # Al presionar este botón, la IA asume la nueva identidad
    if st.button("Cargar Paciente"):
        modelo = genai.GenerativeModel('gemini-1.5-flash', system_instruction=nuevo_prompt)
        st.session_state.chat = modelo.start_chat(history=[])
        st.session_state.chat_history = [
            {"role": "assistant", "content": "(El paciente ha ingresado a la sala. Inicia el interrogatorio)."}
        ]
        # Guardamos los hallazgos en la memoria para los botones del alumno
        st.session_state.fisico_actual = nuevo_fisico
        st.session_state.pocus_actual = nuevo_pocus
        st.rerun()

# Inicialización por defecto (para cuando se abre la página por primera vez)
if "chat_history" not in st.session_state:
    modelo_inicial = genai.GenerativeModel('gemini-1.5-flash', system_instruction=nuevo_prompt)
    st.session_state.chat = modelo_inicial.start_chat(history=[])
    st.session_state.chat_history = [{"role": "assistant", "content": "Doctor, me siento mal..."}]
    st.session_state.fisico_actual = nuevo_fisico
    st.session_state.pocus_actual = nuevo_pocus

# --- INTERFAZ DEL ALUMNO ---
with st.sidebar:
    st.header("🗂️ Acciones Médicas")
    st.markdown("Solicita información adicional:")
    
    if st.button("🔍 Realizar Examen Físico"):
        st.warning(st.session_state.fisico_actual)
        
    if st.button("📟 Realizar POCUS"):
        st.info(st.session_state.pocus_actual)

# Interfaz del chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Interroga al paciente..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        respuesta = st.session_state.chat.send_message(prompt)
        st.markdown(respuesta.text)
        
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta.text})