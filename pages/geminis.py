import streamlit as st
import google.generativeai as genai

# Configura la API Key de Google Generative AI
genai.configure(api_key=st.secrets.GEMINI.api_key)

# Selecciona el modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Crea la interfaz de usuario con Streamlit
st.title("Explicador de Código con Gemini 1.5")
st.write("Ingresa un fragmento de código para obtener comentarios sobre qué hace cada parte.")

# Entrada de código del usuario
user_code = st.text_area("Pega tu código aquí:", height=200)

# Genera la explicación si se presiona el botón
if st.button("Explicar Código"):
    if user_code.strip():
        # Genera la explicación
        prompt = (
            "Analiza el siguiente código y explica, línea por línea, qué hace cada parte:\n\n"
            f"{user_code}"
        )
        response = model.generate_content(prompt)
        
        if response and hasattr(response, "text"):
            st.subheader("Explicación Generada:")
            st.write(response.text)
        else:
            st.write("No se pudo generar una explicación. Inténtalo de nuevo.")
    else:
        st.write("Por favor ingresa un fragmento de código para analizar.")
