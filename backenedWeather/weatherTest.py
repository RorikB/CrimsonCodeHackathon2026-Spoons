import datetime as dt
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "c3104a1428db270a31cf81dfcfb99322"  # your API key
CITY = "Pullman"

def kelvin_to_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9/5) + 32
    return celsius, fahrenheit

# Build request URL (NO spaces)
url = f"{BASE_URL}?appid={API_KEY}&q={CITY}"

# Fetch data
response = requests.get(url).json()

# Extract data
temp_kelvin = response['main']['temp']
temp_celsius, temp_fahrenheit = kelvin_to_fahrenheit(temp_kelvin)

feels_kelvin = response['main']['feels_like']
feels_celsius, feels_fahrenheit = kelvin_to_fahrenheit(feels_kelvin)

wind_speed = response['wind']['speed']
humidity = response['main']['humidity']
description = response['weather'][0]['description']

sunrise_timestamp = dt.datetime.utcfromtimestamp(
    response['sys']['sunrise'] + response['timezone']
)
sunset_timestamp = dt.datetime.utcfromtimestamp(
    response['sys']['sunset'] + response['timezone']
)

# Print output to terminal
print(f"Temperature in {CITY}: {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F")
print(f"Feels like: {feels_celsius:.2f}°C / {feels_fahrenheit:.2f}°F")
print(f"Humidity: {humidity}%")
print(f"Wind Speed: {wind_speed} m/s")
print(f"Weather: {description}")
print(f"Sunrise: {sunrise_timestamp}")
print(f"Sunset: {sunset_timestamp}")