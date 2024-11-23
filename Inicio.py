import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")

# Título y subtítulo
st.title("Proyecto Integrador: SportStock")

# Imagen de fondo
image = Image.open("./static/logo.jpeg")
st.image(image, width=300, use_container_width=True)  

# Integrantes
st.header("Nuestro Equipo")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("./static/Juan-Carlos.png", use_container_width=True)  
    st.write("**Juan Carlos Garcia**")
   

with col2:
    st.image("./static/Bibiana.png",  use_container_width=True)  
    st.write("**Bibiana Machado**")
    

with col3:
    st.image("./static/Duban.png", use_container_width=True)  
    st.write("**Duvan Sanchez**")
    

with col4:
    st.image("./static/Dayana.png", use_container_width=True)  
    st.write("**Dayana Castro Villa**")
    

with col5:
    st.image("./static/camilo.png",  use_container_width=True)  
    st.write("**Juan Camilo Hernandez**")
    

    

# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
Tiene como objetivo principal optimizar la gestion de los productos, controlar el stock de articulos y mejorar la eficiencia operativa de la tienda.""" )


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
