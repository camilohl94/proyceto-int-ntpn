import streamlit as st
import google.generativeai as genai

# Configurar la API de Google Generative AI
genai.configure(api_key='AIzaSyAk9t8cwQn-d_KN7V_D9Z7Njkfvir5TfS8')
modelo = genai.GenerativeModel("gemini-1.5-flash")

# Función para generar respuestas
def generar_respuesta(pregunta, contexto):
    """Genera una respuesta relacionada con el inventario usando IA Gemini."""
    prompt = f"""
    Eres un asistente especializado en la gestión de inventario de gimnasios. 
    Aquí tienes una pregunta o descripción sobre el gimnasio:
    ---
    {pregunta}
    ---
    {contexto}
    Proporciona una respuesta clara, detallada y relevante.
    """
    try:
        respuesta = modelo.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        return f"Error al generar respuesta: {e}"

# Datos del gimnasio (pueden cargarse desde un archivo o base de datos en un proyecto más avanzado)
equipos_gimnasio = {
    "Máquina de remo": {"cantidad": 3, "estado": "Bueno", "último mantenimiento": "2023-10-15"},
    "Pesas libres": {"cantidad": 20, "estado": "Regular", "último mantenimiento": "2024-01-10"},
    "Bicicleta estática": {"cantidad": 5, "estado": "Excelente", "último mantenimiento": "2024-04-01"},
}

# Interfaz en Streamlit
st.title("Gestión de Inventario de Gimnasio  ")
st.write("Consulta el estado de los equipos del gimnasio o solicita recomendaciones.")

# Consultar inventario
st.sidebar.title("Consulta del inventario")
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo:", list(equipos_gimnasio.keys()))

if equipo_seleccionado:
    equipo = equipos_gimnasio[equipo_seleccionado]
    st.sidebar.subheader(f"Detalles de {equipo_seleccionado}")
    st.sidebar.write(f"*Cantidad:* {equipo['cantidad']}")
    st.sidebar.write(f"*Estado:* {equipo['estado']}")
    st.sidebar.write(f"*Último mantenimiento:* {equipo['último mantenimiento']}")

# Pregunta al asistente
pregunta = st.text_area("Describe tu consulta o problema:")
contexto = f"El inventario actual es: {equipos_gimnasio}."

if st.button("Solicitar Respuesta"):
    if pregunta.strip():
        with st.spinner("Procesando con la IA..."):
            respuesta = generar_respuesta(pregunta, contexto)
            st.subheader("Respuesta generada por la IA:")
            st.write(respuesta)
    else:
        st.warning("Por favor, escribe una pregunta válida.")

# Sugerir mantenimiento
st.subheader("Sugerencias de Mantenimiento")
st.write("La IA puede analizar el inventario y sugerir equipos que podrían necesitar mantenimiento.")
if st.button("Analizar inventario"):
    prompt_mantenimiento = f"""
    Basándote en este inventario:
    {equipos_gimnasio}
    Sugiere qué equipos necesitan mantenimiento inmediato o reemplazo.
    """
    with st.spinner("Analizando..."):
        sugerencias = generar_respuesta(prompt_mantenimiento, "")