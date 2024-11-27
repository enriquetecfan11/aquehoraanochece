import streamlit as st
from datetime import datetime
import requests
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title='A qué hora anochece', page_icon='🌙', layout='wide')

# Inicializar variables en session_state
if 'sunset_info' not in st.session_state:
    st.session_state.sunset_info = None
if 'map_data' not in st.session_state:
    st.session_state.map_data = None

st.title('A qué hora anochece')
st.markdown("---")

# Entrada de ubicación y fecha
ubicacion = st.text_input("Ingrese su ubicación:")
fecha = st.date_input("Seleccione la fecha:", datetime.today())

if 'map_data' not in st.session_state:
    st.session_state.map_data = None

if st.button("Obtener hora de la puesta de sol"):
    if not ubicacion:
        st.error("Ubicación no especificada. Por favor, ingrese una ubicación válida.")
    else:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; StreamlitApp/1.0)'}
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={ubicacion}", headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                st.error("No se encontraron coordenadas para la ubicación proporcionada.")
            else:
                lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
                api_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={fecha.strftime('%Y-%m-%d')}&formatted=0"
                response = requests.get(api_url)
                response.raise_for_status()
                data = response.json()

                if data["status"] != "OK":
                    st.error("No se pudo obtener la información de la puesta de sol. Intente nuevamente.")
                else:
                    sunset_time_utc = data["results"]["sunset"]
                    sunset_datetime_utc = datetime.strptime(sunset_time_utc, '%Y-%m-%dT%H:%M:%S+00:00')
                    sunset_time = sunset_datetime_utc.strftime('%H:%M:%S')
                    
                    # Guardar información en session_state
                    st.session_state.sunset_info = {
                        'ubicacion': ubicacion,
                        'fecha': fecha,
                        'sunset_time': sunset_time
                    }
                    st.session_state.map_data = {
                        'lat': lat,
                        'lon': lon
                    }

        except requests.exceptions.RequestException as e:
            st.error(f"Error al obtener los datos: {e}")

# Mostrar resultados si existen en session_state
if st.session_state.sunset_info:
    st.success(f"La hora de la puesta de sol en {st.session_state.sunset_info['ubicacion']} el {st.session_state.sunset_info['fecha'].strftime('%Y-%m-%d')} es a las {st.session_state.sunset_info['sunset_time']} UTC")

# Mostrar el mapa si los datos son válidos
if st.session_state.map_data and 'lat' in st.session_state.map_data and 'lon' in st.session_state.map_data:
    try:
        lat = st.session_state.map_data['lat']
        lon = st.session_state.map_data['lon']
        
        popup_hora = f"Puesta de sol a las {st.session_state.sunset_info['sunset_time']} UTC"

        # Verificar valores de lat y lon
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            m = folium.Map(location=[lat, lon], zoom_start=12, width=800, height=800)  # Ajusta el tamaño del mapa
            folium.Marker([lat, lon], popup=popup_hora).add_to(m)
            map_object = folium.Map(location=[lat, lon], zoom_start=12)
            folium.Marker([lat, lon], popup=ubicacion).add_to(map_object)
            st_folium(m)
        else:
            st.write("Latitud o longitud fuera de rango.")
    except Exception as e:
        st.write(f"Error al renderizar el mapa: {e}")
else:
    st.write("No hay datos para mostrar el mapa.")
