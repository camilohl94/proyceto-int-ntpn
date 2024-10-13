import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  
import datetime  # Para manejar fechas

st.set_page_config(layout="wide")

st.subheader("Proyecto Integrador")

# Verificar si ya existe una instancia de la aplicación
if not firebase_admin._apps:  
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"]  
    secrets_dict = firebase_credentials.to_dict()  
    cred = credentials.Certificate(secrets_dict)  
    app = firebase_admin.initialize_app(cred)

# Obtener el cliente de Firestore
db = firestore.client()

tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico, tab_ventas, tab_dashboard = st.tabs([
    "Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico", "Ventas", "Dashboard"
])

#----------------------------------------------------------
# Descripción
#----------------------------------------------------------
with tad_descripcion:
    st.markdown('''   
    ### Introducción
    - ¿Qué es el proyecto?
    - ¿Cuál es el objetivo principal?
    - ¿Por qué es importante?
    ### Desarrollo
    - Explicación detallada del proyecto
    - Procedimiento utilizado
    - Resultados obtenidos
    ### Conclusión
    - Resumen de los resultados
    - Logros alcanzados
    - Dificultades encontradas
    - Aportes personales
    ''')

#----------------------------------------------------------
# Generador de datos
#----------------------------------------------------------
with tab_Generador:
    st.write('Genera datos ficticios de usuarios y productos y los carga en Firestore.')
    fake = Faker('es_CO')
    ciudades_colombianas = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']

    def generate_fake_users(n):
        users = []
        for _ in range(n):
            user = {
                'nombre': fake.name(),
                'email': fake.email(),
                'edad': random.randint(18, 80),
                'ciudad': random.choice(ciudades_colombianas)
            }
            users.append(user)
        return users

    def generate_fake_products(n):
        categories = {
            'Deportes': ['Pesas', 'Colchoneta de yoga', 'Bicicleta', 'Tenis para correr', 'Guantes de boxeo']
        }
        products = []
        for _ in range(n):
            category = random.choice(list(categories.keys()))
            product_type = random.choice(categories[category])
            product = {
                'nombre': product_type,
                'precio': round(random.uniform(10000, 1000000), -3),
                'categoria': category,
                'stock': random.randint(0, 100)
            }
            products.append(product)
        return products

    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()

    def add_data_to_firestore(collection, data):
        for item in data:
            db.collection(collection).add(item)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Usuarios')
        num_users = st.number_input('Número de usuarios a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Usuarios'):
            delete_collection('usuarios')
            users = generate_fake_users(num_users)
            add_data_to_firestore('usuarios', users)
            st.success(f'{num_users} usuarios añadidos a Firestore')
            st.dataframe(pd.DataFrame(users))

    with col2:
        st.subheader('Productos')
        num_products = st.number_input('Número de productos a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Productos'):
            delete_collection('productos')
            products = generate_fake_products(num_products)
            add_data_to_firestore('productos', products)
            st.success(f'{num_products} productos añadidos a Firestore')
            st.dataframe(pd.DataFrame(products))

#----------------------------------------------------------
# Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Visualiza los datos de usuarios y productos almacenados en Firestore.')
    tab_user, tab_prodcutos = st.tabs(["Usuarios", "Productos"])
    with tab_user:        
        users = db.collection('usuarios').stream()
        users_data = [doc.to_dict() for doc in users]
        df_users = pd.DataFrame(users_data)
        df_users = df_users[['nombre', 'email', 'edad', 'ciudad']]   
        st.dataframe(df_users)

    with tab_prodcutos:       
        products = db.collection('productos').stream()
        products_data = [doc.to_dict() for doc in products]
        df_products = pd.DataFrame(products_data)
        df_products = df_products[['nombre', 'categoria', 'precio', 'stock']]
        st.dataframe(df_products)

#----------------------------------------------------------
# Ventas
#----------------------------------------------------------
with tab_ventas:
    st.subheader("Registro de Ventas")
    
    def register_sale(product_id, quantity_sold):
        product_ref = db.collection('productos').document(product_id)
        product = product_ref.get().to_dict()
        new_stock = max(product['stock'] - quantity_sold, 0)
        product_ref.update({'stock': new_stock})
        
        sale = {
            'producto_id': product_id,
            'cantidad': quantity_sold,
            'fecha': datetime.datetime.now(),
            'precio_total': product['precio'] * quantity_sold
        }
        db.collection('ventas').add(sale)
        return sale
    
    product_id = st.text_input('ID del Producto')
    quantity_sold = st.number_input('Cantidad Vendida', min_value=1)
    if st.button('Registrar Venta'):
        sale = register_sale(product_id, quantity_sold)
        st.write(f"Venta registrada: {sale}")

#----------------------------------------------------------
# Dashboard
#----------------------------------------------------------
with tab_dashboard:
    st.title("Dashboard del Inventario y Ventas")

    def get_inventory_statistics():
        total_products = db.collection('productos').get().size
        low_stock_products = db.collection('productos').where('stock', '<', 5).get().size
        total_sales = db.collection('ventas').get().size
        total_income = sum([sale.to_dict()['precio_total'] for sale in db.collection('ventas').get()])
        return total_products, low_stock_products, total_sales, total_income

    total_products, low_stock_products, total_sales, total_income = get_inventory_statistics()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Productos', total_products)
    col2.metric('Productos con Bajo Stock', low_stock_products)
    col3.metric('Total Ventas', total_sales)
    col4.metric('Total Ingresos', total_income)

    st.subheader('Productos con Bajo Stock')
    low_stock_products = db.collection('productos').where('stock', '<', 5).stream()
    low_stock_data = [doc.to_dict() for doc in low_stock_products]
    if low_stock_data:
        st.dataframe(pd.DataFrame(low_stock_data))
    else:
        st.write("No hay productos con stock bajo.")
