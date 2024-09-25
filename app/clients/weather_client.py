import requests
from urllib.parse import urljoin
from app.settings import settings

class WeatherClient:
    def __init__(self):
        self.base_url = settings.weather_api_base_url
        self.api_key = settings.api_key

    def get_city_weather(self, city: str) -> dict:
        try:
            url = urljoin(self.base_url, city)
            response = requests.get(url, params={'key': self.api_key})
            response.raise_for_status()
            data = response.json()
            return data
        except requests.HTTPError as ex:
            raise Exception(f"Error fetching weather data for {city}: {ex.response.status_code} - {ex.response.text}")
