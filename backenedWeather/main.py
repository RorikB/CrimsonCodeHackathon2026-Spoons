import datetime as dt
import requests

Base_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open('c3104a1428db270a31cf81dfcfb99322', 'r').read()
CITY = "Pullman"


def Kelvin_to_Fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9/5) + 32
    return celsius, fahrenheit

url = Base_URL + "appid= " + API_KEY + "&q=" + CITY

reponse = requests.get(url).json()

temp_kelvin = reponse['main']['temp']
temp_celsius, temp_fahrenheit = Kelvin_to_Fahrenheit(temp_kelvin)
feels_kelvin = reponse['main']['feels_like']
feels_celsius, feels_fahrenheit = Kelvin_to_Fahrenheit(feels_kelvin)
wind_speed = reponse['wind']['speed']
humidity = reponse['main']['humidity']
description = reponse['weather'][0]['description']
sunrise_timestamp = dt.datetime.utcfromtimestamp(reponse['sys']['sunrise'] + reponse['timezone'])  
sunset_timestamp = dt.datetime.utcfromtimestamp(reponse['sys']['sunset'] + reponse['timezone'])

print(f"Temperature: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
print(f"Temperature in {CITY} feels like: {feels_celsius:.2f}°C or {feels_fahrenheit:.2f}°F")
print(f"Humidity in {CITY}: {humidity}%")
print(f"wind speed in {CITY}: {wind_speed} m/s")
print (f"General weather {CITY}: {description}")
print( f"sun rises in {CITY}: at {sunrise_timestamp} local time")
print(f"sun sets in {CITY}:  at {sunset_timestamp} local time")


print(reponse)