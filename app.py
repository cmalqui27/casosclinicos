import streamlit as st
import time

# Configuración de la página
st.set_page_config(page_title="Simulador de Casos Clínicos", page_icon="🩺", layout="wide")

st.title("🩺 Simulador Clínico: Sala de Hospitalización")
st.markdown("Interroga al paciente, solicita exámenes y define un plan de trabajo.")

# --- BARRA LATERAL (Información del Paciente y Signos Vitales) ---
with st.sidebar:
    st.header("📋 Ficha del Paciente")
    st.write("**Nombre:** Juan Pérez")
    st.write("**Edad:** 68 años")
    st.write("**Motivo de consulta:** Falta de aire")
    
    st.divider()
    st.subheader("📊 Signos Vitales de Ingreso")
    st.write("- **PA:** 140/90 mmHg")
    st.write("- **FC:** 110 lpm")
    st.write("- **FR:** 24 rpm")
    st.write("- **SpO2:** 88% (FiO2 0.21)")
    st.write("- **T°:** 36.8 °C")

    st.divider()
    # Botones para que el alumno pida información extra
    if st.button("Ver Hallazgos POCUS"):
        st.info("Patrón B difuso bilateral en insonación pulmonar. VCI pletórica sin colapso inspiratorio.")
    
    if st.button("Solicitar Laboratorio"):
        st.warning("El laboratorio aún está procesando la muestra. (Intenta más tarde)")

# --- INTERFAZ DE CHAT ---
# Inicializar el historial de chat en la memoria de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola doctor... me falta mucho el aire. Siento el pecho apretado."}
    ]

# Mostrar los mensajes históricos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caja de texto para que el alumno pregunte
if prompt := st.chat_input("Escribe tu pregunta para el paciente aquí..."):
    # Mostrar la pregunta del alumno
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simular la respuesta del paciente (Aquí conectaremos la IA más adelante)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Respuesta temporal de prueba
        respuesta_simulada = "Me empezó anoche, doctor. No podía dormir acostado, tuve que sentarme en el borde de la cama."
        
        # Efecto de escritura
        full_response = ""
        for chunk in respuesta_simulada.split():
            full_response += chunk + " "
            time.sleep(0.1)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})