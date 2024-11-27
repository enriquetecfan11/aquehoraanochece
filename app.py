import streamlit as st
from datetime import datetime, timedelta
import requests

st.set_page_config(
    page_title='A qué hora anochece',
    page_icon='🌙',
    layout='wide',
    initial_sidebar_state='auto'
)

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

st.title('A qué hora anochece')
st.markdown("---")

col1, col2 = st.columns([1, 1])  # Cambia 'columns' por 'beta_columns'
lat, lon = None, None

with col1:
    ubicacion = st.text_input("Ingrese su ubicación:")
    fecha = st.date_input("Seleccione la fecha:", datetime.today())
    if st.button("Obtener hora de la puesta de sol", key='get_sunset_time'):
        if not ubicacion:
            st.error("Ubicación no especificada. Por favor, ingrese una ubicación válida.")
            st.stop()

        try:
            # Obtener coordenadas usando Nominatim
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={ubicacion}")
            response.raise_for_status()
            data = response.json()
            if not data:
                st.error("No se encontraron coordenadas para la ubicación proporcionada.")
                st.stop()

            lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
            api_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={fecha.strftime('%Y-%m-%d')}&formatted=0"
        except Exception as e:
            st.error(f"Error al obtener las coordenadas: {e}")
            st.stop()

        try:
            # Obtener datos de la puesta de sol
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if data["status"] != "OK":
                st.error("No se pudo obtener la información de la puesta de sol. Intente nuevamente.")
                st.stop()

            sunset_time_utc = data["results"]["sunset"]
            sunset_datetime_utc = datetime.strptime(sunset_time_utc, '%Y-%m-%dT%H:%M:%S+00:00')
            sunset_datetime_user_timezone = sunset_datetime_utc + timedelta(hours=1)  # UTC+1
            st.success(f"La hora de la puesta de sol en {ubicacion} el {fecha.strftime('%Y-%m-%d')} es a las {sunset_datetime_user_timezone.strftime('%H:%M:%S')} UTC+1")
        except Exception as e:
            st.error(f"Error al obtener la información de la puesta de sol: {e}")
            st.stop()

        try:
            # Obtener información meteorológica
            api_key = '959d55cbfd41bca8951a491bde080a8c'
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            if weather_data['cod'] != 200:
                st.error("No se pudo obtener información meteorológica. Intente nuevamente.")
                st.stop()

            weather_description = weather_data['weather'][0]['description'].capitalize()
            temperature = weather_data['main']['temp']
            temperature_celsius = temperature - 273.15  # Convertir a Celsius

            st.markdown("### Información meteorológica en tiempo real:")
            st.markdown(f"El clima en {ubicacion} es {weather_description} con una temperatura de {temperature_celsius:.2f}°C")
        except Exception as e:
            st.error(f"Error al obtener la información meteorológica: {e}")



with col2:
  if lat is not None and lon is not None:

      # Obtener mapa usando la API de OpenStreetMap con un zoom de 12x
    st.markdown("### Mapa de la ubicación:")
    map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-0.05}%2C{lat-0.05}%2C{lon+0.05}%2C{lat+0.05}&amp;layer=mapnik&amp;marker={lat}%2C{lon}"
    st.components.v1.iframe(map_url, height=400)
  
  else:
    st.error("Ubicación no especificada. Por favor, ingrese una ubicación válida.")