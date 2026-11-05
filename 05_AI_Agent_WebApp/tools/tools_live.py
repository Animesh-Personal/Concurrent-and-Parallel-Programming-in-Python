import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str):
    """
    Fetches the weather information for a given city. Return
    Temperature in Fahrenheit for locations in US, Liberia, Burma etc.
    """

    print("Fetching weather information from weather API...get_weather() tool")

    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,  
        "appid": api_key,
        "units": "metric"
        }

    request = requests.get(base_url, params=params)
    data = request.json()
    temperature_celsius = data['main']['temp']
    temperature_fahrenheit = (temperature_celsius * 9/5) + 32
    return data, {"temperature_fahrenheit": temperature_fahrenheit}

def get_location():
    """
    Fetches the current location of the user.
    """
    print("Fetching location from IP API...get_location() tool")

    from flask import session
    user_lat = session['user_session']['lat']
    user_lon = session['user_session']['lon']
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={user_lat}&lon={user_lon}",
                            headers={"User-Agent": "WeatherApp/1.0"}, timeout=5)   

    data = response.json()
    city = data['address'].get('city', data['address'].get('town', 'Unknown'))
    country = data['address'].get('country', '')
    return f"{city}, {country}"