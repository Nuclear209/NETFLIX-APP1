
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

# Cargar las credenciales de Firestore desde los secretos de Streamlit
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="Netflix02")

# Función para filtrar por título
def filter_by_name(name, data):
    return data[data['name'].str.contains(name, case=False, na=False)]

# Función para filtrar por director
def filter_by_director(director, data):
    return data[data['director'] == director]

# Mostrar los datos si el usuario selecciona la opción
if st.sidebar.checkbox('Mostrar todos los filmes'):
    st.subheader('Todos los filmes')
    
    # Recuperar los datos de Firestore (colección de filmes)
    films_ref = db.collection("films")  # Cambia "films" por el nombre de tu colección
    films = list(films_ref.stream())  # Recuperamos todos los documentos de la colección
    films_dict = [film.to_dict() for film in films]  # Convertir los documentos en un diccionario
    data = pd.DataFrame(films_dict)  # Convertir los diccionarios en un DataFrame

    st.dataframe(data)  # Mostrar todos los filmes

# Entrada de texto para buscar filmes
titulofilme = st.sidebar.text_input('Título del filme:')
btnBuscar = st.sidebar.button('Buscar filmes')

# Filtrar los filmes por título
if btnBuscar and titulofilme:
    if 'data' in locals() and not data.empty:
        data_filme = filter_by_title(titulofilme, data)
        count_row = data_filme.shape[0]  # Número de filas
        st.write(f"Total de filmes encontrados: {count_row}")
        if not data_filme.empty:
            st.dataframe(data_filme)
    else:
        st.warning("No se han cargado los datos aún.")

# Filtrar los filmes por director
selected_director = st.sidebar.selectbox("Seleccionar Director", data['director'].unique() if 'data' in locals() else [])
btnFilterbyDirector = st.sidebar.button('Filtrar por Director')

if btnFilterbyDirector and selected_director:
    if 'data' in locals() and not data.empty:
        filtered_by_director = filter_by_director(selected_director, data)
        count_row = filtered_by_director.shape[0]  # Número de filas
        st.write(f"Total de filmes de {selected_director}: {count_row}")
        if not filtered_by_director.empty:
            st.dataframe(filtered_by_director)
    else:
        st.warning("No se han cargado los datos aún.")

# Mostrar los datos de Firestore (otra colección si es necesario)
names_ref = db.collection("names")  # Cambia "names" por la colección que necesites
names = list(names_ref.stream())
names_dict = [name.to_dict() for name in names]
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

