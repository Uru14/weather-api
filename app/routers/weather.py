from fastapi import APIRouter, HTTPException
from app.clients.weather_client import WeatherClient
import redis
from app.settings import settings

router = APIRouter()

redis_client = redis.StrictRedis.from_url(settings.redis_url)
weather_client = WeatherClient()

@router.get("/weather/{city}")
async def get_weather(city: str):
    cached_weather = redis_client.get(city)

    if cached_weather:
        return eval(cached_weather.decode('utf-8'))

    try:
        data = weather_client.get_city_weather(city)
    except Exception:
        raise HTTPException(status_code=503, detail="Error fetching weather data")

    weather_data = {
        "city": city,
        "temperature": data['currentConditions']['temp'],
        "description": data['currentConditions']['conditions']
    }

    redis_client.set(city, str(weather_data), ex=43200)
    return weather_data
