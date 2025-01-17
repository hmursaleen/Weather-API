import requests
from django.conf import settings

def fetch_weather_data(city_name):
    """
    Fetch weather data from the third-party API.
    :param city_name: Name of the city to fetch weather data for
    :return: Parsed weather data (dict) or None if an error occurs
    """
    api_key = settings.WEATHER_API_KEY
    base_url = settings.WEATHER_API_BASE_URL

    try:
        url = f"{base_url}/{city_name}?unitGroup=metric&key={api_key}&contentType=json"
        
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return {
            "city": city_name,
            "temperature": f"{data['currentConditions']['temp']}°C",
            "feels_like": f"{data['currentConditions']['feelslike']}°C",
            "description": data['currentConditions']['conditions'],
            "humidity": f"{data['currentConditions']['humidity']}%",
            "wind_speed": f"{data['currentConditions']['windspeed']} km/h",
        }
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
