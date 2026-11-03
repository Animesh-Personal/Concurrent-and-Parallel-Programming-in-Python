import os
import requests

def get_weather(city: str):
    """
    Fetches the weather information for a given city. Return
    Temperature in Fahrenheit for locations in US, Liberia, Burma etc.
    """
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
    response = requests.get("https://ipapi.co/json/", headers = {'User-agent': 'your-bot 0.1'})
    data = response.json()
    city = data['city']
    country = data.get('country_name')
    return f"{city}, {country}"