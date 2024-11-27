import streamlit as st
from datetime import datetime, timedelta
import requests
from timezonefinder import TimezoneFinder
import pytz
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title='A qué hora anochece',
    page_icon='🌙',
    layout='wide',
    initial_sidebar_state='auto'
)

# CSS personalizado para mejorar el estilo de la página
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        color: #333333;
    }
    .container {
        max-width: 800px;
        margin: auto;
    }
    .button {
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 5px;
        background-color: #3498db;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la aplicación
st.title('A qué hora anochece')
st.markdown("---")

# Dividir la pantalla en dos columnas para separar la entrada de datos y el mapa
col1, col2 = st.columns([1, 1])
lat, lon = None, None

with col1:
    # Entrada de ubicación y fecha
    ubicacion = st.text_input("Ingrese su ubicación:")
    fecha = st.date_input("Seleccione la fecha:", datetime.today())
    if st.button("Obtener hora de la puesta de sol", key='get_sunset_time'):
        if not ubicacion:
            # Mostrar error si no se ha ingresado la ubicación
            st.error("Ubicación no especificada. Por favor, ingrese una ubicación válida.")
            st.stop()

        try:
            # Obtener coordenadas usando Nominatim (servicio de OpenStreetMap)
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={ubicacion}")
            response.raise_for_status()
            data = response.json()
            if not data:
                # Mostrar error si no se encontraron resultados para la ubicación
                st.error("No se encontraron coordenadas para la ubicación proporcionada.")
                st.stop()

            # Extraer latitud y longitud de los resultados
            lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
            
            # Obtener la zona horaria utilizando TimezoneFinder
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lat=lat, lng=lon)
            if not timezone_str:
                # Mostrar error si no se puede determinar la zona horaria
                st.error("No se pudo determinar la zona horaria de la ubicación.")
                st.stop()
            timezone = pytz.timezone(timezone_str)
            
            # Preparar la URL para obtener los datos de la puesta de sol
            api_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={fecha.strftime('%Y-%m-%d')}&formatted=0"
        except requests.exceptions.RequestException as e:
            # Manejar errores relacionados con la solicitud HTTP
            st.error(f"Error al obtener las coordenadas: {e}")
            st.stop()
        except ValueError:
            # Manejar errores relacionados con la conversión de datos
            st.error("Error al procesar los datos de la ubicación. Por favor, intente con otra ubicación.")
            st.stop()

        try:
            # Obtener datos de la puesta de sol usando la API sunrise-sunset
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if data["status"] != "OK":
                # Mostrar error si no se pudo obtener la información de la puesta de sol
                st.error("No se pudo obtener la información de la puesta de sol. Intente nuevamente.")
                st.stop()

            # Convertir la hora de la puesta de sol de UTC a la hora local del usuario
            sunset_time_utc = data["results"]["sunset"]
            sunset_datetime_utc = datetime.strptime(sunset_time_utc, '%Y-%m-%dT%H:%M:%S+00:00')
            sunset_datetime_local = sunset_datetime_utc.astimezone(timezone)
            
            # Mostrar la hora de la puesta de sol en la zona horaria local
            st.success(f"La hora de la puesta de sol en {ubicacion} el {fecha.strftime('%Y-%m-%d')} es a las {sunset_datetime_local.strftime('%H:%M:%S')} ({timezone_str})")
        except requests.exceptions.RequestException as e:
            # Manejar errores relacionados con la solicitud HTTP
            st.error(f"Error al obtener la información de la puesta de sol: {e}")
            st.stop()
        except ValueError:
            # Manejar errores relacionados con la conversión de datos
            st.error("Error al procesar los datos de la puesta de sol. Por favor, intente nuevamente.")
            st.stop()

        try:
            # Obtener información meteorológica usando OpenWeatherMap API
            api_key = '959d55cbfd41bca8951a491bde080a8c'
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            if weather_data['cod'] != 200:
                # Mostrar error si no se pudo obtener la información meteorológica
                st.error("No se pudo obtener información meteorológica. Intente nuevamente.")
                st.stop()

            # Extraer y convertir la descripción del clima y la temperatura
            weather_description = weather_data['weather'][0]['description'].capitalize()
            temperature = weather_data['main']['temp']
            temperature_celsius = temperature - 273.15  # Convertir de Kelvin a Celsius

            # Mostrar la información meteorológica al usuario
            st.markdown("### Información meteorológica en tiempo real:")
            st.markdown(f"El clima en {ubicacion} es {weather_description} con una temperatura de {temperature_celsius:.2f}°C")
        except requests.exceptions.RequestException as e:
            # Manejar errores relacionados con la solicitud HTTP
            st.error(f"Error al obtener la información meteorológica: {e}")
        except ValueError:
            # Manejar errores relacionados con la conversión de datos
            st.error("Error al procesar los datos meteorológicos. Por favor, intente nuevamente.")

with col2:
    # Mostrar el mapa de la ubicación si se han obtenido las coordenadas
    if lat is not None and lon is not None:
        st.markdown("### Mapa de la ubicación:")
        # Crear el mapa usando Folium centrado en la ubicación especificada
        map_object = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=ubicacion).add_to(map_object)
        # Mostrar el mapa en la aplicación
        st_folium(map_object, width=700, height=400)
    else:
        # Mostrar advertencia si no hay ubicación especificada
        st.warning("Por favor, ingrese una ubicación para ver el mapa.")
