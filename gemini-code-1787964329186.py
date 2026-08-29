import streamlit as st
import google.generativeai as genai

# Configuración de la API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Simulador Clínico", page_icon="🩺", layout="wide")
st.title("🩺 Simulador Clínico Interactivo")

# --- MODO DOCENTE ---
with st.expander("⚙️ PANEL DOCENTE (Configurar Nuevo Caso)", expanded=False):
    st.markdown("Escribe aquí los detalles del paciente. Los alumnos no verán esto.")
    nuevo_prompt = st.text_area(
        "1. Reglas de la IA (El Prompt):", 
        value="Eres Roberto, 65 años. Tienes mareos al usar el brazo izquierdo. No des tu diagnóstico. Responde corto.", 
        height=100
    )
    nuevo_fisico = st.text_input("2. Examen Físico:", value="PA Brazo Derecho: 140/85 | Brazo Izquierdo: 95/60")
    nuevo_pocus = st.text_input("3. Hallazgos POCUS:", value="Flujo retrógrado en arteria vertebral izquierda.")
    
    if st.button("Cargar Paciente"):
        # Usamos la versión universal que no genera errores 404
        modelo = genai.GenerativeModel('gemini-pro')
        
        # Inyectamos las instrucciones de forma manual como el primer mensaje oculto
        historial_oculto = [
            {"role": "user", "parts": [f"INSTRUCCIONES ESTRICTAS PARA TI: {nuevo_prompt}. ¿Entendido?"]},
            {"role": "model", "parts": ["Entendido. Actuaré como el paciente a partir de ahora."]}
        ]
        st.session_state.chat = modelo.start_chat(history=historial_oculto)
        st.session_state.chat_history = [{"role": "assistant", "content": "Doctor, qué bueno que viene... me siento muy mareado, parece que me voy a caer."}]
        st.session_state.fisico_actual = nuevo_fisico
        st.session_state.pocus_actual = nuevo_pocus
        st.rerun()

# --- INICIALIZACIÓN POR DEFECTO ---
if "chat_history" not in st.session_state:
    modelo_inicial = genai.GenerativeModel('gemini-pro')
    historial_oculto = [
        {"role": "user", "parts": ["INSTRUCCIONES ESTRICTAS: Eres Roberto, 65 años. Tienes mareos al usar el brazo izquierdo. No des tu diagnóstico. Responde corto. ¿Entendido?"]},
        {"role": "model", "parts": ["Entendido. Actuaré como el paciente a partir de ahora."]}
    ]
    st.session_state.chat = modelo_inicial.start_chat(history=historial_oculto)
    st.session_state.chat_history = [{"role": "assistant", "content": "Doctor, me siento mal..."}]
    st.session_state.fisico_actual = "PA Brazo Derecho: 140/85 | Brazo Izquierdo: 95/60"
    st.session_state.pocus_actual = "Flujo retrógrado en arteria vertebral izquierda."

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
    # Guardar y mostrar lo que pregunta el alumno
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # El modelo responde
    with st.chat_message("assistant"):
        respuesta = st.session_state.chat.send_message(prompt)
        st.markdown(respuesta.text)
        
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta.text})