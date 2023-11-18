import streamlit as st
from datetime import datetime, timedelta
import requests

# Página principal
st.set_page_config(page_title='A qué hora anochece', page_icon='🌙', layout='wide', initial_sidebar_state='auto')


# Agregar un campo de búsqueda de ubicación
ubicacion = st.text_input("Ingrese su ubicación:")

# Obtener latitud y longitud de la ubicación ingresada
if ubicacion:
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={ubicacion}")
        data = response.json()
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        # Only get the first result
        # Only get 2 decimal places
        latnew = round(float(lat), 2)
        lonnew = round(float(lon), 4)

    except Exception as e:  
        st.error(f"Error al obtener las coordenadas: {e}")

# Agregar un campo de fecha
fecha = st.date_input("Seleccione la fecha que ver cuando anochece:", datetime.today())

# Botón para obtener la hora de la puesta de sol
if st.button("Obtener hora de la puesta de sol"):
    # Construir la URL para la API de sunrise-sunset.org
    api_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={fecha.strftime('%Y-%m-%d')}&formatted=0"

    # Verificar si la ubicación no está vacía
    if ubicacion:
        # Intentar obtener las coordenadas usando algún servicio de geocodificación
        try:
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={ubicacion}")
            data = response.json()
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

        print('UTC: ', sunset_datetime_user_timezone)

        # Pasar de utc a utc+1
        sunset_datetime_user_timezone_1 = datetime.strptime(sunset_datetime_user_timezone, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
        # Pero solo quiero la hora
        sunset_datetime_user_timezone_1 = sunset_datetime_user_timezone_1.strftime('%H:%M:%S')

        print('UTC +1 : ', sunset_datetime_user_timezone_1)

        
        st.success(f"La hora de la puesta de sol en {ubicacion} el dia {fecha.strftime('%Y-%m-%d')} es a las {sunset_datetime_user_timezone_1}")
        st.write(f"Las coordenadas de {ubicacion} son ({latnew}, {lonnew})")
    else:
        st.error("Hubo un error al obtener la información. Por favor, inténtalo de nuevo.")