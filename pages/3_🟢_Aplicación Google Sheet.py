import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

st.set_page_config(layout="wide")

st.subheader("Filtrador de Datos del Metro de Medellín")

st.markdown(""" 
Tasas de mortalidad según enfermedades respiratorias y circulatorias calculadas en el proyecto 
Calidad del aire y sus efectos en la salud de la población de los diez municipios del valle de aburrá
""")

st.write('1pyWrBdeFBrwbdnJZ_DHW0MpzXDYWvfux1LouNppqYeM')

# Configuración de Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = st.text_input("ID hoja de cálculo")
RANGE1 = "Sheet1!A:E"  
RANGE2 = "Sheet2!A:E"  

# Configuración de credenciales
google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
secrets_dict = google_sheet_credentials.to_dict()
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def read_sheet():
    """Lee los datos de Sheet1"""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    
    if values:
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
    return pd.DataFrame()

def update_sheet(df):
    """Actualiza Sheet2 con los datos filtrados"""
    if not df.empty:
        try:
            # Primero limpiamos la hoja 2
            sheet.values().clear(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE2
            ).execute()
            
            # Luego actualizamos con los nuevos datos
            values = [df.columns.tolist()] + df.values.tolist()
            body = {'values': values}
            
            result = sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE2,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            return result
        except Exception as e:
            st.error(f"Error al actualizar: {str(e)}")
            return None
    else:
        st.error("No hay datos para actualizar")
        return None

# Usar session state para mantener los datos entre rerenders
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None

# Botón para cargar datos
if st.button("Leer"):
    df = read_sheet()
    
    if not df.empty:
        st.header("Datos Hoja1")
        st.dataframe(df)
        
        filtro = df[
            ((df['Municipio'] == 'Bello') | (df['Municipio'] == 'Medellin')) & 
            ((df['Año'] == '2010') | (df['Año'] == '2017')) &  
            ((df['Enfermedad'] == 'Enfermedades respiratorias')|(df['Enfermedad'] == 'Enfermedades circulatorias')) &
            (df['Sexo'] == 'Hombres')
        ]
        
       
        st.session_state.filtered_data = filtro

        st.header('Filtros realizado')
        st.dataframe(filtro)
    else:
        st.error("No se encontraron datos en la hoja de cálculo")


if st.session_state.filtered_data is not None:
    if st.button('Actualizar Hoja2'):
        result = update_sheet(st.session_state.filtered_data)
        if result:
            st.success(f'Datos actualizados correctamente: {result["updatedCells"]} celdas.')