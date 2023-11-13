import streamlit as st
from datetime import datetime
import requests
import folium
from streamlit_folium import folium_static

# Página principal
st.title("¿A qué hora anochece?")

# Agregar un campo de búsqueda de ubicación
ubicacion = st.text_input("Ingrese su ubicación:")

# Agregar un campo de fecha
fecha = st.date_input("Seleccione la fecha:", datetime.today())

# Mapa interactivo
mapa = folium.Map(location=[47.776, 1.672], zoom_start=8)

# Botón para obtener la hora de la puesta de sol
if st.button("Obtener hora de la puesta de sol"):
    # Construir la URL para la API de sunrise-sunset.org
    api_url = f"https://api.sunrise-sunset.org/json?lat=0&lng=0&date={fecha.strftime('%Y-%m-%d')}&formatted=0"
    if ubicacion:
        # Intentar obtener las coordenadas usando algún servicio de geocodificación
        try:
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={ubicacion}")
            data = response.json()
            if data:
                lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
                # Actualizar el mapa con la nueva ubicación
                mapa.location = [lat, lon]
                mapa.zoom_start = 20
                folium.Marker([lat, lon], popup=ubicacion).add_to(mapa)

        except Exception as e:
            st.error(f"Error al obtener las coordenadas: {e}")

    # Hacer la solicitud a la API
    response = requests.get(api_url)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if data["status"] == "OK":
        sunset_time_utc = data["results"]["sunset"]
        
        # Convertir la hora de la puesta de sol a un objeto datetime
        sunset_datetime_utc = datetime.strptime(sunset_time_utc, '%Y-%m-%dT%H:%M:%S+00:00')

        # Convertir la hora de la puesta de sol a la zona horaria del usuario
        sunset_datetime_user_timezone = sunset_datetime_utc.strftime('%Y-%m-%d %H:%M:%S')
        
        st.success(f"La hora de la puesta de sol en {ubicacion} el {fecha.strftime('%Y-%m-%d')} es a las {sunset_datetime_user_timezone}")
    else:
        st.error("Hubo un error al obtener la información. Por favor, inténtalo de nuevo.")

# Mostrar el mapa en la interfaz de Streamlit
folium_static(mapa)
