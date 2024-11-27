# Sunset Time - Streamlit App

This Streamlit app allows users to get the sunset time and weather information for a specific location. It also displays an interactive map of the provided location using `Folium`. The app leverages multiple APIs to provide accurate sunset and weather data.

## Features

- **Sunset Time**: Enter a location and a date to get the time of sunset.
- **Weather Information**: Provides current weather conditions, including a description and temperature for the specified location.
- **Interactive Map**: Displays an interactive map of the entered location using `Folium`.

## Technologies Used

- **Streamlit**: A Python framework for creating interactive web applications.
- **Nominatim (OpenStreetMap)**: Converts the entered location into geographic coordinates (latitude and longitude).
- **TimezoneFinder**: Determines the correct timezone based on coordinates.
- **Sunrise-Sunset API**: Retrieves sunset times in UTC format.
- **OpenWeatherMap API**: Provides weather information for the specified location.
- **Folium**: Visualizes interactive maps.

## Prerequisites

- Python 3.7 or higher
- A valid API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys)

## How to Run

To run the app locally, activate your virtual environment and execute the following command:

```sh
streamlit run app.py
```

This will open the app in your browser, where you can enter a location and date to retrieve the desired information.

## Notes

- **Custom User-Agent**: The request to Nominatim (OpenStreetMap) includes a custom `User-Agent` header to avoid usage restrictions.
- **Error Handling**: The app includes error handling for common issues like missing results, connectivity errors, and data processing problems.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Author

Created by [Enrique Rodriguez Vela](https://github.com/enriqutecfan11).

