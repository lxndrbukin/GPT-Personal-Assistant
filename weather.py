from dotenv import load_dotenv
import os
import requests

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather(city=None):
    city = city or "Birmingham, UK"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    current_temp = response.json()["main"]["temp"]
    feels_like = response.json()["main"]["feels_like"]
    weather_desc = response.json()["weather"][0]["description"]
    humidity = response.json()["main"]["humidity"]
    return f"It's {round(current_temp)}°C in {city} with {weather_desc}. Feels like {round(feels_like)}°C and humidity at {humidity}%."