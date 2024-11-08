import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

tad_descripcion, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------- -----------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      
    st.markdown('''
    ## Análisis de hábitos de entrenamiento y salud en un gimnasio

    ### Introducción

    -   ¿Qué es el proyecto?
    
    El proyecto busca transformar los datos en conocimiento útil para mejorar la gestión del gimnasio 
    y ofrecer un servicio más personalizado y efectivo a sus usuarios.
    
    -   ¿Cuál es el objetivo principal?
     
     Queremos utilizar los datos para crear un perfil detallado del usuario típico del gimnasio,
     identificar tendencias y patrones en su comportamiento, 
     y comprender qué los motiva a seguir entrenando.
    -   ¿Por qué es importante? 
    
     Al comprender a fondo el comportamiento de nuestros usuarios nos permite ofrecer una experiencia más personalizada y satisfactoria, 
     lo que a su vez conduce a un aumento de la satisfacción del cliente, la retención y el crecimiento del negocio.

    ### Desarrollo

    -   Explicación detallada del proyecto
    
    Nuestro objetivo principal es comprender a fondo el comportamiento de los usuarios de un gimnasio
     a través del análisis de datos detallados
     sobre sus hábitos de entrenamiento, características físicas y preferencias.
     Al analizar esta información, podemos obtener datos valiosos que nos permitan
     mejorar la experiencia del usuario, optimizar las operaciones del gimnasio
     y tomar decisiones de negocio más informadas

    
    -   Procedimiento utilizado
    
    Carga de datos: pandas.read_csv: Para leer datos desde un archivo CSV y almacenarlos en un DataFrame.
    df.head(): Para visualizar las primeras filas del DataFrame
    matplotlib.pyplot y seaborn: Para crear gráficos como histogramas y diagramas de caja.
    streamlit: Para crear una interfaz de usuario interactiva y mostrar los resultados.
    pandas: Para seleccionar columnas, filtrar datos, realizar cálculos y otras operaciones sobre el DataFrame.
    
    -   Resultados obtenidos
    
    Dimensiones: Número de filas y columnas del conjunto de datos (a través de df.shape).
    Tipos de datos: El tipo de dato de cada columna (con df.dtypes).
    Resumen estadístico: Medidas como la media, mediana, desviación estándar,
    valores mínimo y máximo de las columnas numéricas (con df.describe()).
    Frecuencia de valores: El número de veces que aparece cada valor único
    en una columna categórica (con df['columna_categorica'].value_counts()).

    ### Conclusión

    -   Resumen de los resultados
    -   Logros alcanzados
    -   Dificultades encontradas
    -   Aportes personales
    ''')    

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio: 
    st.title("Análisis Exploratorio")
    st.markdown("""
    * Muestra las primeras 5 filas del DataFrame.  **(df.head())**
    * Muestra la cantidad de filas y columnas del DataFrame.  **(df.shape)**
    * Muestra los tipos de datos de cada columna.  **(df.dtypes)**
    * Identifica y muestra las columnas con valores nulos. **(df.isnull().sum())**
    * Muestra un resumen estadístico de las columnas numéricas.  **(df.describe())**
    * Muestra una tabla con la frecuencia de valores únicos para una columna categórica seleccionada. **(df['columna_categorica'].value_counts())** 
    * Otra información importante           
    """)   

    # Cargar el DataFrame desde un archivo CSV
    df = pd.read_csv('./static/datasets/DataGYM.csv', sep=';')   # Asegúrate de cambiar la ruta al archivo correcto

    def mostrar_resultados(df, consulta):
        """Muestra los resultados de la consulta seleccionada.

        Args:
            df (pd.DataFrame): DataFrame con los datos.
            consulta (str): Consulta seleccionada por el usuario.
        """
        if consulta == 'Mostrar las primeras 5 filas':
            st.write('Primeras 5 filas:')
            st.dataframe(df.head())
        elif consulta == 'Cantidad de filas y columnas':
            st.write('Dimensiones del DataFrame:')
            st.write(df.shape)
        elif consulta == 'Tipos de datos de cada columna':
            st.write('Tipos de datos:')
            st.write(df.dtypes)
        elif consulta == 'Mostrar columnas con valores nulos':
            st.write('Valores nulos por columna:')
            st.write(df.isnull().sum())
        elif consulta == 'Resumen estadístico de las columnas numéricas':
            st.write('Resumen estadístico:')
            st.write(df.describe())
        elif consulta == 'Frecuencia de valores únicos para una columna':
            columna = st.selectbox('Selecciona una columna:', df.columns)
            if columna in df.select_dtypes(include=['object']).columns:
                st.write(f"Frecuencia de valores únicos para '{columna}':")
                st.bar_chart(df[columna].value_counts())
            else:
                st.warning(f"La columna '{columna}' no es categórica.")
        elif consulta == 'Visualizar distribución de una variable numérica':
            columna = st.selectbox('Selecciona una columna numérica:', df.select_dtypes(include=['number']).columns)
            fig, ax = plt.subplots()
            sns.histplot(data=df, x=columna, kde=True)
            st.pyplot(fig)

    # Lista de opciones para el selectbox
    consultas_seleccionadas = [
        "Selecciona una consulta",  # Opción predeterminada
        "Mostrar las primeras 5 filas",
        "Cantidad de filas y columnas",
        "Tipos de datos de cada columna",
        "Mostrar columnas con valores nulos",
        "Resumen estadístico de las columnas numéricas",
        "Frecuencia de valores únicos para una columna",
        "Visualizar distribución de una variable numérica"
    ]

    # Crear el selectbox para el usuario
    consulta = st.selectbox('Selecciona una consulta:', consultas_seleccionadas)

    # Mostrar los resultados de la consulta seleccionada
    if consulta != "Selecciona una consulta":
        mostrar_resultados(df, consulta)



#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------
with tab_Filtrado_Básico:
        st.title("Filtro Básico")
        st.markdown("""
        * Permite filtrar datos usando condiciones simples. **(df[df['columna'] == 'valor'])**
        * Permite seleccionar una columna y un valor para el filtro. **(st.selectbox, st.text_input)**
        * Permite elegir un operador de comparación (igual, diferente, mayor que, menor que). **(st.radio)**
        * Muestra los datos filtrados en una tabla. **(st.dataframe)** 
        """)
 

#----------------------------------------------------------
#Analítica 3
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)



    




