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


tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio,  tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtro Final Dinámico"])

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
                'fecha': str(fake.date_this_year()),
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
        num_products = st.number_input('Número de productos a generar', min_value=1, max_value=200, value=10)
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
        num_movements = st.number_input('Número de movimientos a generar', min_value=1, max_value=200, value=10)
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
    tab_movimientos, tab_prodcutos = st.tabs(["Movimientos", "Prodcutos"])
    with tab_movimientos:        
        # Obtener datos de una colección de Firestore
        movimientos = db.collection('movimientos_inventario').stream()
        # Convertir datos a una lista de diccionarios
        movimientos_data = [doc.to_dict() for doc in movimientos]
        # Crear DataFrame
        df_movimientos = pd.DataFrame(movimientos_data)
        # Reordenar las columnas
        column_order_movimientos = ['producto', 'tipo', 'cantidad', 'fecha','responsable']
        df_movimientos = df_movimientos.reindex(columns=column_order_movimientos)   
        st.dataframe(df_movimientos)
    with tab_prodcutos:       
        
        productos = db.collection('productos').stream()
        # Convertir datos a una lista de diccionarios
        productos_data = [doc.to_dict() for doc in productos]
        # Crear DataFrame
        df_products = pd.DataFrame(productos_data)
         # Reordenar las columnas
        column_order = ['nombre', 'categoria', 'precio', 'stock']
        df_products = df_products.reindex(columns=column_order)
        
        st.dataframe(df_products)

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
# Análisis Exploratorio para la tabla de movimientos
with tab_Análisis_Exploratorio:
    st.title("Análisis Exploratorio tabla movimientos")
    st.markdown("""
    Selecciona la operación que deseas realizar con la tabla de movimientos:
    """)

    # Lista de opciones
    opciones_movimientos = [
        'Mostrar las primeras 5 filas', 
        'Cantidad de filas y columnas', 
        'Tipos de datos de cada columna', 
        'Mostrar columnas con valores nulos', 
        'Resumen estadístico de las columnas numéricas', 
        'Frecuencia de valores únicos para "tipo"'
    ]
    
    # Crear el selectbox para elegir una opción
    opcion_movimientos = st.selectbox('Elige una opción:', opciones_movimientos, key='movimientos')

    if df_movimientos.empty:
        st.warning('No hay datos para mostrar en la tabla de movimientos.')
    else:
        # Mostrar datos según la opción seleccionada
        if opcion_movimientos == 'Mostrar las primeras 5 filas':
            st.write('Primeras 5 filas de la tabla movimientos:')
            st.dataframe(df_movimientos.head())

        elif opcion_movimientos == 'Cantidad de filas y columnas':
            st.write('Cantidad de filas y columnas de la tabla movimientos:')
            st.write(df_movimientos.shape)

        elif opcion_movimientos == 'Tipos de datos de cada columna':
            st.write('Tipos de datos de cada columna:')
            st.write(df_movimientos.dtypes)

        elif opcion_movimientos == 'Mostrar columnas con valores nulos':
            st.write('Columnas con valores nulos:')
            st.write(df_movimientos.isnull().sum())

        elif opcion_movimientos == 'Resumen estadístico de las columnas numéricas':
            st.write('Resumen estadístico de las columnas numéricas:')
            st.write(df_movimientos.describe())

        elif opcion_movimientos == 'Frecuencia de valores únicos para "tipo"':
            if 'tipo' in df_movimientos.columns:
                st.write("Frecuencia de valores únicos para 'tipo':")
                st.dataframe(df_movimientos['tipo'].value_counts())
            else:
                st.warning("La columna 'tipo' no existe en el DataFrame de movimientos.")


# Análisis Exploratorio para la tabla de productos
with tab_Análisis_Exploratorio:
    st.title("Análisis Exploratorio tabla productos")
    st.markdown("""
    Selecciona la operación que deseas realizar con la tabla de productos:
    """)

    # Lista de opciones
    opciones_productos = [
        'Mostrar las primeras 5 filas', 
        'Cantidad de filas y columnas', 
        'Tipos de datos de cada columna', 
        'Mostrar columnas con valores nulos', 
        'Resumen estadístico de las columnas numéricas', 
        'Frecuencia de valores únicos para "categoria"'
    ]
    
    # Crear el selectbox para elegir una opción
    opcion_productos = st.selectbox('Elige una opción:', opciones_productos, key='productos')

    if df_products.empty:
        st.warning('No hay datos para mostrar en la tabla de productos.')
    else:
        # Mostrar datos según la opción seleccionada
        if opcion_productos == 'Mostrar las primeras 5 filas':
            st.write('Primeras 5 filas de la tabla productos:')
            st.dataframe(df_products.head())

        elif opcion_productos == 'Cantidad de filas y columnas':
            st.write('Cantidad de filas y columnas de la tabla productos:')
            st.write(df_products.shape)

        elif opcion_productos == 'Tipos de datos de cada columna':
            st.write('Tipos de datos de cada columna:')
            st.write(df_products.dtypes)

        elif opcion_productos == 'Mostrar columnas con valores nulos':
            st.write('Columnas con valores nulos:')
            st.write(df_products.isnull().sum())

        elif opcion_productos == 'Resumen estadístico de las columnas numéricas':
            st.write('Resumen estadístico de las columnas numéricas:')
            st.write(df_products.describe())

        elif opcion_productos == 'Frecuencia de valores únicos para "categoria"':
            if 'categoria' in df_products.columns:
                st.write("Frecuencia de valores únicos para 'categoria':")
                st.dataframe(df_products['categoria'].value_counts())
            else:
                st.warning("La columna 'categoria' no existe en el DataFrame de productos.")
        


with tab_Filtro_Final_Dinámico:
    st.title("Filtro Final Dinámico")
    st.markdown("""
    * Permite filtrar datos usando condiciones simples.
    * Selecciona una tabla, luego una columna, un valor de filtro y un operador de comparación.
    * Muestra los datos filtrados en una tabla.
    """)

    # Crear un selectbox para que el usuario elija la tabla
    tabla_seleccionada = st.selectbox('Selecciona la tabla para aplicar el filtro:', ['Movimientos', 'Productos'])

    # Selección del DataFrame según la tabla seleccionada
    if tabla_seleccionada == 'Movimientos':
        df = df_movimientos
        nombre_tabla = "movimientos"
    else:
        df = df_products
        nombre_tabla = "productos"

    if df.empty:
        st.warning(f'No hay datos disponibles para filtrar en la tabla {nombre_tabla}.')
    else:
        columnas = df.columns.tolist()
        columna_seleccionada = st.selectbox(f'Selecciona una columna para filtrar ({nombre_tabla}):', columnas)

        valor_filtro = st.text_input(f'Introduce el valor para filtrar la columna {columna_seleccionada} ({nombre_tabla}):')

        operadores = ['Igual', 'Diferente', 'Mayor que', 'Menor que']
        operador_seleccionado = st.radio(f'Selecciona el operador de comparación ({nombre_tabla}):', operadores)

        if valor_filtro:
            try:
                # Convertir el valor de filtro si es numérico
                valor_filtro = float(valor_filtro) if valor_filtro.replace('.', '', 1).isdigit() else valor_filtro

                # Aplicar el filtro según el operador seleccionado
                if operador_seleccionado == 'Igual':
                    df_filtrado = df[df[columna_seleccionada] == valor_filtro]
                elif operador_seleccionado == 'Diferente':
                    df_filtrado = df[df[columna_seleccionada] != valor_filtro]
                elif operador_seleccionado == 'Mayor que':
                    df_filtrado = df[df[columna_seleccionada] > valor_filtro]
                elif operador_seleccionado == 'Menor que':
                    df_filtrado = df[df[columna_seleccionada] < valor_filtro]

                # Guardar el DataFrame filtrado en el session_state
                st.session_state['df_filtrado'] = df_filtrado

                st.write(f'Datos filtrados por {columna_seleccionada} {operador_seleccionado} {valor_filtro} ({nombre_tabla}):')
                st.dataframe(df_filtrado)

            except ValueError:
                st.error(f'El valor de filtro introducido no es válido para la columna {columna_seleccionada} en la tabla {nombre_tabla}.')

   
    if 'df_filtrado' in st.session_state:
        df_final = st.session_state['df_filtrado']

        if df_final.empty:
            st.warning('No hay datos filtrados para mostrar.')
        else:
            st.write(f"Resumen del DataFrame filtrado:")
            st.write(f"Total de filas después del filtro: {df_final.shape[0]}")
            st.write(f"Total de columnas: {df_final.shape[1]}")

            # Mostrar la tabla filtrada
            st.dataframe(df_final)

            # Mostrar estadísticas
            st.write("Resumen estadístico de las columnas numéricas:")
            st.write(df_final.describe())

            # Mostrar gráficos si hay datos suficientes
            if df_final.select_dtypes(include='number').shape[1] > 0:
                st.write("Gráfico de distribución de las columnas numéricas:")
                st.bar_chart(df_final.select_dtypes(include='number'))

            if 'categoria' in df_final.columns or 'tipo' in df_final.columns:
                col_categ = 'categoria' if 'categoria' in df_final.columns else 'tipo'
                st.write(f"Frecuencia de valores únicos para '{col_categ}':")
                st.bar_chart(df_final[col_categ].value_counts())

    else:
        st.warning("No se han aplicado filtros aún. Usa las pestañas anteriores para aplicar filtros y ver los resultados aquí.")



