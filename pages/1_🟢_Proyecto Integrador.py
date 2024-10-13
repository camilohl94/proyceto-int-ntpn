import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  

st.set_page_config(layout="wide")

st.subheader("Proyecto Integrador")

# Verificar si ya existe una instancia de la aplicación
if not firebase_admin._apps:  
    # Cargar las credenciales de Firebase desde los secretos de Streamlit
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"]  
    # Convertir las credenciales a un diccionario Python
    secrets_dict = firebase_credentials.to_dict()  
    # Crear un objeto de credenciales usando el diccionario 
    cred = credentials.Certificate(secrets_dict)  
    # Inicializar la aplicación de Firebase con las credenciales
    app = firebase_admin.initialize_app(cred)

# Obtener el cliente de Firestore
db = firestore.client()


tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''   

    ### Introducción

    -   ¿Qué es el proyecto?
    -   ¿Cuál es el objetivo principal?
    -   ¿Por qué es importante?

    ### Desarrollo

    -   Explicación detallada del proyecto
    -   Procedimiento utilizado
    -   Resultados obtenidos

    ### Conclusión

    -   Resumen de los resultados
    -   Logros alcanzados
    -   Dificultades encontradas
    -   Aportes personales
    ''')

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tab_Generador:
    
    fake = Faker('es_CO')

    def generate_fake_gym_products(n):
        categories = {
            'Máquinas': [
                'Bicicleta estática', 'Cinta de correr', 'Máquina de remo', 
                'Elíptica', 'Máquina de pesas', 'Banco de pesas', 'Polea', 
                'Máquina Smith', 'Prensa de pierna', 'Escaladora'
            ],
            'Accesorios': [
                'Mancuernas', 'Pesas rusas', 'Colchoneta de yoga', 'Banda de resistencia', 
                'Guantes de gimnasio', 'Cuerda para saltar', 'Rueda abdominal', 
                'Discos de pesas', 'Pesa ajustable', 'Soporte para pesas'
            ],
            'Suplementos': [
                'Proteína en polvo', 'Creatina', 'Aminoácidos BCAA', 'Pre-entreno', 
                'Multivitamínico', 'Barritas energéticas', 'Glutamina', 'Omega 3', 
                'Quemadores de grasa', 'Carbohidratos'
            ]
        }

        products = []
        for _ in range(n):
            category = random.choice(list(categories.keys()))
            product_type = random.choice(categories[category])
            
            product = {
                'nombre': product_type,
                'precio': round(random.uniform(50000, 2000000), -3),  
                'categoria': category,
                'stock': random.randint(0, 50)
            }
            products.append(product)
        return products

    
    def generate_fake_inventory_movements(n, products):
        movements = []
        movement_types = ['Entrada', 'Salida']
        
        for _ in range(n):
            product = random.choice(products)  
            movement_type = random.choice(movement_types)
            quantity = random.randint(1, 10)
            movement = {
                'producto': product['nombre'],
                'tipo': movement_type,
                'cantidad': quantity,
                'fecha': fake.date_this_year(),
                'responsable': fake.name()
            }
            movements.append(movement)
        return movements

    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()

    def add_data_to_firestore(collection, data):
        for item in data:
            db.collection(collection).add(item)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Productos')
        num_products = st.number_input('Número de productos a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Productos'):
            with st.spinner('Eliminando productos existentes...'):
                delete_collection('productos')
            with st.spinner('Generando y añadiendo nuevos productos...'):
                products = generate_fake_gym_products(num_products)
                add_data_to_firestore('productos', products)
            st.success(f'{num_products} productos añadidos a Firestore')
            st.dataframe(pd.DataFrame(products))

    with col2:
        st.subheader('Movimientos de Inventario')
        num_movements = st.number_input('Número de movimientos a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Movimientos'):
            with st.spinner('Eliminando movimientos existentes...'):
                delete_collection('movimientos_inventario')
            with st.spinner('Generando y añadiendo nuevos movimientos...'):
                products = db.collection('productos').get() 
               

                if not products:
                    st.warning('No hay productos disponibles en firestore.')
                else:
                    product_list=[{'nombre': p.to_dict()['nombre']} for p in products]
                    movements = generate_fake_inventory_movements(num_movements,product_list)
                    add_data_to_firestore('movimientos_inventario',movements)
                    st.success(f'{num_movements} movimientos añadidos a firestore')
                    st.dataframe(pd.DataFrame(movements))



#----------------------------------------------------------
#Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Esta función muestra datos de usuarios y productos almacenados en una base de datos Firestore, permitiendo una visualización organizada y fácil acceso a la información.')
    tab_user, tab_prodcutos = st.tabs(["Usuarios", "Prodcutos"])
    with tab_user:        
        # Obtener datos de una colección de Firestore
        users = db.collection('usuarios').stream()
        # Convertir datos a una lista de diccionarios
        users_data = [doc.to_dict() for doc in users]
        # Crear DataFrame
        df_users = pd.DataFrame(users_data)
        # Reordenar las columnas
        column_order = ['nombre', 'email', 'edad', 'ciudad']
        df_users = df_users.reindex(columns=column_order)   

        st.dataframe(df_users)
    with tab_prodcutos:       
        # Obtener datos de una colección de Firestore
        users = db.collection('productos').stream()
        # Convertir datos a una lista de diccionarios
        users_data = [doc.to_dict() for doc in users]
        # Crear DataFrame
        df_products = pd.DataFrame(users_data)
         # Reordenar las columnas
        column_order = ['nombre', 'categoria', 'precio', 'stock']
        df_products = df_products.reindex(columns=column_order)
        
        st.dataframe(df_products)

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
#Analítica 2
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)


