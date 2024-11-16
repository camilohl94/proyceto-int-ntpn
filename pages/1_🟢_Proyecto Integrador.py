import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import matplotlib.pyplot as plt
import seaborn as sns
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
#Descripción
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''   

    ### Introducción

    -  **¿Qué es el proyecto?**
        El proyecto de sistema de inventario es una iniciativa que busca diseñar, desarrollar e implementar
        un sistema que permita gestionar y controlar de manera eficiente los bienes y productos de una organización. 
                
    -   **¿Cuál es el objetivo principal?**
         El objetivo principal de un sistema de inventario es optimizar la gestión de existencias para garantizar que
         los productos estén disponibles cuando se necesiten, minimizando al mismo tiempo costos y desperdicios.
                
    -   **¿Por qué es importante?**
         La implementación de un sistema de inventario es importante por varias razones:
        * Mejor control de stock 
        * Optimización de costos 
        * Toma de decisiones informada
        * Mejora en la satisfacción del cliente
        * Eficiencia operativa
        * Cumplimiento normativo
        * Análisis de rendimiento

    ### Desarrollo

    -   **Explicación detallada del proyecto**
        Este sistema incluye la recopilación de datos sobre la cantidad, ubicación y estado de los inventarios,
        así como la automatización de procesos relacionados con la entrada, salida y seguimiento de los mismos.
                
    -   **Procedimiento utilizado**
        **Análisis de Requisitos:**
         * Reunir información sobre las necesidades específicas de la empresa.
         * Identificar las funcionalidades que el sistema debe tener.
        
        **Diseño del sistema:**
         * Crear un diseño que incluya la estructura de la base de datos, interfaces y flujos de trabajo.
         * Planificar la arquitectura del sistema y la integración con otros sistemas existentes.

        **Desarrollo:**
         * Programar el software utilizando lenguajes y tecnologías apropiadas.
         * Desarrollar módulos específicos, como gestión de entradas y salidas, reportes y análisis.

        **Pruebas:** 
         * Realizar pruebas funcionales y de usuario para asegurarse de que el sistema cumple con los requisitos.
         * Identificar y corregir errores o problemas antes de la implementación.
                
    -   **Resultados obtenidos**
         **Control preciso del inventario:** Evita excesos y escasez.
         **Reducción de costos:** Minimiza gastos de almacenamiento y deterioro.
         **Optimización del flujo de efectivo:** Mantiene niveles óptimos de inversión en inventario.
         **Mejora en la toma de decisiones:** Facilita decisiones informadas sobre compras y ventas.
         **Mayor satisfacción del cliente:** Asegura disponibilidad de productos.
         **Reducción de pérdidas:** Previene vencimientos y deterioros.
         **Automatización:** Ahorra tiempo y reduce errores. 

    ### Conclusión

    -   **Resumen de los resultados**
         En conjunto, estos resultados permiten una gestión más eficiente, reducen costos y mejoran la productividad y
         la competitividad del negocio.
                
    -   **Logros alcanzados**
         * Stock óptimo sin excesos ni faltantes.
         * Reducción de costos de almacenamiento y pérdidas.
         * Eficiencia operativa y automatización de tareas.
         * Mejor toma de decisiones con datos en tiempo real.
         * Mayor satisfacción del cliente al asegurar disponibilidad.
         Estos logros reflejan una gestión de inventario más controlada, rentable y orientada a la satisfacción del cliente.
                
    -   **Dificultades encontradas**
         * Errores de registro: Datos incorrectos por errores humanos o técnicos.
         * Integración con otros sistemas: Complejidad para enlazar el inventario con otros procesos, como ventas y contabilidad.
         * Falta de datos en tiempo real: Problemas de actualización que afectan la precisión del inventario.
                
    -   **Aportes personales**
         * Análisis crítico: Identificación de áreas de mejora.
         * Innovación: Propuestas de nuevas funcionalidades.
         * Resolución de problemas: Manejo de obstáculos durante la implementación.
         * Feedback Constructivo: Retroalimentación para mejoras continuas.
         * Adaptabilidad: Flexibilidad ante cambios en el proyecto.
         * Compromiso: Dedicación para asegurar el éxito del sistema.
    ''')

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tab_Generador:
    
    fake = Faker('es_CO')

    def generate_fake_gym_products(n):
        categories = {
            'Máquinas': [
                'Bicicleta estática', 'Cinta de correr', 'Máquina de remo', 'Elíptica', 
                'Máquina de pesas', 'Banco de pesas', 'Polea', 'Máquina Smith', 
                'Prensa de pierna', 'Escaladora', 'Prensa de pecho', 'Máquina de dorsales', 
                'Multiestación', 'Caminadora eléctrica', 'Máquina de abdominales', 
                'Máquina de glúteos', 'Stepper', 'Rack de sentadillas', 'Extensión de piernas', 
                'Flexión de piernas', 'Máquina de abductores', 'Máquina de aductores', 
                'Máquina de pantorrillas', 'Máquina de isquiotibiales', 'Máquina de gemelos', 
                'Máquina de prensa de hombros', 'Máquina de remo asistida', 'Máquina de trapecios', 
                'Máquina de hiperextensiones', 'Máquina de empuje de cadera'
                ],
           'Accesorios': [
                'Mancuernas', 'Pesas rusas', 'Colchoneta de yoga', 'Banda de resistencia', 
                'Guantes de gimnasio', 'Cuerda para saltar', 'Rueda abdominal', 'Discos de pesas', 
                'Pesa ajustable', 'Soporte para pesas', 'Rodillo de espuma', 'Step de aerobic', 
                'Tobilleras con peso', 'Bola de estabilidad', 'Cinturón de levantamiento', 
                'Protector de muñeca', 'Pesa de tobillo', 'Bandas elásticas', 'Agarres para dominadas', 
                'Alfombrilla antideslizante', 'Tobilleras ajustables', 'Rueda de equilibrio', 
                'Barra para dominadas', 'Chaleco con peso', 'Balón medicinal', 'Escalera de agilidad', 
                'Tobilleras de peso ajustables', 'Arnés para resistencia', 'Soporte para estiramiento', 
                'Soporte para flexiones'
                ],
            'Suplementos': [
                'Proteína en polvo', 'Creatina', 'Aminoácidos BCAA', 'Pre-entreno', 
                'Multivitamínico', 'Barritas energéticas', 'Glutamina', 'Omega 3', 
                'Quemadores de grasa', 'Carbohidratos', 'Electrolitos', 'Beta alanina', 
                'Cafeína', 'Colágeno hidrolizado', 'Proteína vegana', 'Vitaminas B12', 
                'Ácido fólico', 'Calcio', 'Magnesio', 'Vitamina D', 'ZMA (Zinc y Magnesio)', 
                'L-arginina', 'MCT Oil', 'Spirulina', 'Extracto de té verde', 'Aceite de pescado', 
                'Suero de leche', 'Suplemento de electrolitos', 'L-carnitina', 'Ashwagandha'
                ]
                 
         }

        unique_products = set()
        products = []

        while len(products) < n and len(unique_products) < sum(len(v) for v in categories.values()):
            category = random.choice(list(categories.keys()))
            product_type = random.choice(categories[category])
            
            if product_type not in unique_products:
                unique_products.add(product_type)
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
        num_products = st.number_input('Número de productos a generar', min_value=1, max_value=87, value=10, step=1, key='num_products')
        if st.button('Generar y Añadir Productos'):
            with st.spinner('Eliminando productos existentes...'):
                delete_collection('Productos')
            with st.spinner('Generando y añadiendo nuevos productos...'):
                products = generate_fake_gym_products(num_products)
                add_data_to_firestore('Productos', products)
            st.success(f'{num_products} productos añadidos a Firestore')
            st.dataframe(pd.DataFrame(products))

    with col2:
        st.subheader('Movimientos de Inventario')
        num_movements = st.number_input('Número de movimientos a generar', min_value=1, max_value=100, value=10, step=1, key='num_movements')
        if st.button('Generar y Añadir Movimientos'):
            with st.spinner('Eliminando movimientos existentes...'):
                delete_collection('Movimientos')
            with st.spinner('Generando y añadiendo nuevos movimientos...'):
                products = db.collection('Productos').get() 
               

                if not products:
                    st.warning('No hay productos disponibles en Firestore.')
                else:
                    product_list=[{'nombre': p.to_dict()['nombre']} for p in products]
                    movements = generate_fake_inventory_movements(num_movements, product_list)
                    add_data_to_firestore('Movimientos',movements)
                    st.success(f'{num_movements} movimientos añadidos a Firestore')
                    st.dataframe(pd.DataFrame(movements))

#----------------------------------------------------------
#Datos
#----------------------------------------------------------
with tab_datos:
    tab_movimientos, tab_productos = st.tabs(["Movimientos", "Productos"])
    with tab_movimientos:        
        # Obtener datos de una colección de Firestore
        movimientos = db.collection('Movimientos').stream()
        # Convertir datos a una lista de diccionarios
        movimientos_data = [doc.to_dict() for doc in movimientos]
        # Crear DataFrame
        df_movimientos = pd.DataFrame(movimientos_data)
        if not df_movimientos.empty:
            # Reordenar las columnas si existen
            column_order_movimientos = ['producto','cantidad', 'fecha', 'tipo','responsable']
            df_movimientos = df_movimientos.reindex(columns=column_order_movimientos)   
        st.dataframe(df_movimientos)
    with tab_productos:       
        productos = db.collection('Productos').stream()
        # Convertir datos a una lista de diccionarios
        productos_data = [doc.to_dict() for doc in productos]
        # Crear DataFrame
        df_products = pd.DataFrame(productos_data)
         # Reordenar las columnas si existen
        column_order = ['nombre', 'categoria', 'precio', 'stock']
        df_products = df_products.reindex(columns=column_order)
        st.dataframe(df_products)

#----------------------------------------------------------
#Análisis Exploratorio
#----------------------------------------------------------
with tab_Análisis_Exploratorio:
    # Análisis Exploratorio para la tabla de movimientos
    st.header("Análisis Exploratorio")
    sub_tabs = st.tabs(["Movimientos", "Productos"])
    
    with sub_tabs[0]:
        st.subheader("Tabla Movimientos")
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
                    st.bar_chart(df_movimientos['tipo'].value_counts())
                else:
                    st.warning("La columna 'tipo' no existe en el DataFrame de movimientos.")

    with sub_tabs[1]:
        st.subheader("Tabla Productos")
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
                    st.bar_chart(df_products['categoria'].value_counts())
                else:
                    st.warning("La columna 'categoria' no existe en el DataFrame de productos.")

#----------------------------------------------------------
#Filtro Final Dinámico Mejorado
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
    st.title("Visualización Dinámica Simplificada")

    st.markdown("""
    **Instrucciones:**
    1. Selecciona una tabla para visualizar.
    2. Elige un tipo de gráfico.
    3. Aplica un filtro opcional (si lo deseas) y observa los resultados.
    """)

    # Selección de tabla
    tabla_seleccionada = st.selectbox(
        'Selecciona la tabla para visualizar:',
        options=['Movimientos', 'Productos']
    )

    if tabla_seleccionada == 'Movimientos':
        df = df_movimientos.copy()  
    elif tabla_seleccionada == 'Productos':
        df = df_products.copy() 

    if df.empty:
        st.warning(f'No hay datos disponibles en la tabla {tabla_seleccionada}.')
    else:
        col1, col2 = st.columns(2)

        with col1:
            # Selección del tipo de gráfico
            tipo_grafico = st.selectbox('Selecciona el tipo de gráfico:', ['Barras', 'Línea', 'Puntos', 'Boxplot'])
        
        with col2:
            # Selección de columnas para la gráfica
            columnas = df.columns.tolist()
            x_columna = st.selectbox('Selecciona la variable para el eje X:', options=columnas)
            y_columna = st.selectbox('Selecciona la variable para el eje Y:', options=columnas)

        # Filtro opcional por columna
        filtro_columna = st.multiselect(f"Filtrar por {x_columna}:", options=['Todos'] + df[x_columna].unique().tolist())
        
        # Si se seleccionan filtros, aplicarlos
        if filtro_columna != ['Todos'] and filtro_columna:
            df = df[df[x_columna].isin(filtro_columna)]

        # Estilos de gráficos con Seaborn
        estilo_grafico = st.selectbox("Selecciona el estilo del gráfico:", options=['darkgrid', 'whitegrid', 'dark', 'white', 'ticks'])
        paleta_colores = st.selectbox("Selecciona la paleta de colores:", options=['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind'])

        sns.set_style(estilo_grafico)
        sns.set_palette(paleta_colores)

        # Crear el gráfico
        st.subheader("Gráfico de Datos")
        fig, ax = plt.subplots(figsize=(10, 6))

        if tipo_grafico == 'Barras':
            sns.barplot(x=x_columna, y=y_columna, data=df, ax=ax)
        elif tipo_grafico == 'Línea':
            sns.lineplot(x=x_columna, y=y_columna, data=df, marker='o', ax=ax)
        elif tipo_grafico == 'Puntos':
            sns.scatterplot(x=x_columna, y=y_columna, data=df, ax=ax)
        elif tipo_grafico == 'Boxplot':
            sns.boxplot(x=x_columna, y=y_columna, data=df, ax=ax)

        ax.set_xlabel(x_columna)
        ax.set_ylabel(y_columna)
        ax.set_title(f'{y_columna} vs {x_columna} ({tipo_grafico})')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("Datos Filtrados")
        st.dataframe(df)