import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")

# Título y subtítulo
st.title("Proyecto Integrador: SportStock")

# Imagen de fondo
image = Image.open("static\proyecto integrador.png")
st.image(image, width=700, use_container_width=True)  

# Integrantes
st.header("Nuestro Equipo")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("./static/Juan-Carlos.png", width=200, use_container_width=True)  
    st.write("**[Juan Carlos Garcia]**")
    st.write("[Colaborador]")

with col2:
    st.image("./static/Camiloj.png", width=123, use_container_width=True)  
    st.write("**[Juan Camilo Hernandez]**")
    st.write("[Colaborador]")

with col3:
    st.image("./static/Duban.png", width=123, use_container_width=True)  
    st.write("**[Duvan Sanchez]**")
    st.write("[Colaborador]")

with col4:
    st.image("./static/Dayana.png", width=150, use_container_width=True)  
    st.write("**[Dayana Castro Villa]**")
    st.write("[Colaboradora]")

with col5:
    st.image("./static/Bibiana.png", width=175, use_container_width=True)  
    st.write("**[Bibiana Machado]**")
    st.write("[Colaboradora]")

# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
Tiene como objetivo principal optimizar la gestion de los productos, controlar el stock de articulos y mejorar la eficiencia operativa de la tienda.""" )


# Footer con links
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.google.com">Google</a> |
        <a href="https://www.facebook.com">Facebook</a> |
        <a href="https://www.linkedin.com">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
