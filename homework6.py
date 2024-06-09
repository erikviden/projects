import json
import datetime
import requests
from geopy.geocoders import Nominatim


class WeatherForecast:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def __setitem__(self, date, forecast):
        if date not in self.data:
            self.data[date] = forecast
            self._save_data()

    def __getitem__(self, date):
        return self.data.get(date, "No forecast available")

    def __iter__(self):
        return iter(self.data.keys())

    def items(self):
        for date, forecast in self.data.items():
            yield date, forecast


def get_latitude_longitude(city):
    geolocator = Nominatim(user_agent="weather_forecast_app")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        print("Location not found.")
        return None, None


def fetch_weather(date, latitude, longitude):
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=rain_sum&start_date={date}&end_date={date}"
    response = requests.get(URL)
    return response.json()


def main():
    weather_forecast = WeatherForecast()

    city = input("Enter a city: ")
    latitude, longitude = get_latitude_longitude(city)
    if latitude is None or longitude is None:
        return

    print(f"Latitude: {latitude}, Longitude: {longitude}")

    date = input("Enter a date in YYYY-MM-DD format to check the weather: ")
    if not date:
        current_date = datetime.date.today()
        date = (current_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    if date not in weather_forecast:
        weather_data = fetch_weather(date, latitude, longitude)
        rain_sum = weather_data["daily"]["rain_sum"][0] if "daily" in weather_data and "rain_sum" in weather_data[
            "daily"] else None
        weather_forecast[date] = {"rain_sum": rain_sum}

    forecast = weather_forecast[date]
    rain_sum = forecast["rain_sum"]
    if rain_sum is not None:
        if rain_sum > 0.0:
            print(f"{date}: Rain in {city}.")
        else:
            print(f"{date}: No rain in {city}.")
    else:
        print("Weather data not available.")

    print("\nSaved weather forecasts:")
    for date, forecast in weather_forecast.items():
        print(f"{date}: {forecast}")


if __name__ == "__main__":
    main()