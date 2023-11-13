import streamlit as st
import requests
from datetime import datetime

# Página principal
st.title("¿A qué hora anochece?")

# Agregar un campo de búsqueda de ubicación
ubicacion = st.text_input("Ingrese su ubicación:")

# Obtener la ubicación del usuario
if st.button("Detectar ubicación"):
    # Aquí puedes usar algún servicio de geolocalización o simplemente pedir al usuario que ingrese manualmente
    # En este ejemplo, asumimos que el usuario ingresa la ubicación manualmente
    st.warning("¡La detección automática de ubicación no está implementada en este ejemplo!")

# Agregar un campo de fecha
fecha = st.date_input("Seleccione la fecha:", datetime.today())

# Botón para obtener la hora de la puesta de sol
if st.button("Obtener hora de la puesta de sol"):
    # Construir la URL para la API de sunrise-sunset.org
    api_url = f"https://api.sunrise-sunset.org/json?lat=0&lng=0&date={fecha.strftime('%Y-%m-%d')}&formatted=0"
    if ubicacion:
        # Si se proporciona la ubicación, intentar obtener las coordenadas usando algún servicio de geocodificación
        # En este ejemplo, simplemente usamos 0,0 como coordenadas si no hay detección de ubicación.
        api_url = f"https://api.sunrise-sunset.org/json?lat=0&lng=0&date={fecha.strftime('%Y-%m-%d')}&formatted=0"

    # Hacer la solicitud a la API
    response = requests.get(api_url)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if data["status"] == "OK":
        sunset_time = data["results"]["sunset"]
        st.success(f"La hora de la puesta de sol en {ubicacion} el {fecha.strftime('%Y-%m-%d')} es a las {sunset_time}")
    else:
        st.error("Hubo un error al obtener la información. Por favor, inténtalo de nuevo.")
