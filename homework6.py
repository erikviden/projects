import requests
from pprint import pprint
import json
import datetime
import geopy

saved_data = {}
def get_latitude_longitude(city):
    geolocator = geopy.Nominatim(user_agent=".")
    location = geolocator.geocode(city)
    if location:
        latitude = int(location.latitude)
        longitude = int(location.longitude)
        return latitude, longitude
    else:
        print("Location not found.")
        return None, None


def get_weather(date, latitude, longitude):
    try:
        with open("data.json", "r") as file_stream:
            data = json.load(file_stream)
            if date and latitude and longitude in data:
                return data[date][latitude][longitude]
    except FileNotFoundError:
        pass

while True:
    city = input("Enter a city: ")
    latitude, longitude = get_latitude_longitude(city)
    if latitude is not None and longitude is not None:
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        break

coordinates = get_latitude_longitude(city)


date = input("Enter a date in YYYY-MM-DD format to check the weather: ")

if date:
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&daily=rain_sum&start_date={date}&end_date={date}"
    response = requests.get(URL)
    data_from_url = response.json()
    with open("data.json", mode="w") as file_stream:
        data_as_json = json.dumps(data_from_url)
        file_stream.write(data_as_json)

elif not date:
    current_date = datetime.date.today()
    next_day = current_date + datetime.timedelta(days=1)
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&daily=rain_sum&start_date={next_day}&end_date={next_day}"
    response = requests.get(URL)
    data_from_url = response.json()
    with open("data.json", mode="w") as file_stream:
        data_as_json = json.dumps(data_from_url)
        file_stream.write(data_as_json)

with open("data.json", mode="r") as file_stream:
    data_as_json = file_stream.read()
    data = json.loads(data_as_json)


rain_sum = data["daily"]["rain_sum"]
rain_sum = rain_sum[0]

if rain_sum > 0.0 :
    print(f"{date} rain in {city}.")
elif rain_sum == 0.0:
    print(f"{date} no rain in {city}.")
else:
    print("I don't know")