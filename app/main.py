import os
import requests
import redis
from fastapi import FastAPI, HTTPException, Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("API_KEY")

# Configuración de Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.StrictRedis.from_url(REDIS_URL)
    # Testear la conexión con un ping
    redis_client.ping()
except redis.ConnectionError:
    raise HTTPException(status_code=500, detail="Redis connection error")

@app.get("/weather/{city}")
async def get_weather(city: str = Path(..., min_length=1, description="Name of the city to fetch the weather")):
    # Validación de entrada
    if not city.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")

    # Buscar en caché los datos del clima
    try:
        cached_weather = redis_client.get(city)
        if cached_weather:
            return eval(cached_weather.decode('utf-8'))
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

    # Solicitud a la API de clima de terceros
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Levanta un error si la respuesta HTTP fue un error
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error fetching data from weather API: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Error decoding JSON from weather API")

    # Verificar si la ciudad fue encontrada en la respuesta
    if 'errorCode' in data:
        raise HTTPException(status_code=404, detail="City not found")

    # Formatear los datos del clima
    weather_data = {
        "city": city,
        "temperature": data['currentConditions']['temp'],
        "description": data['currentConditions']['conditions']
    }

    # Almacenar los datos en Redis con expiración de 12 horas
    try:
        redis_client.set(city, str(weather_data), ex=43200)  # 43200 segundos = 12 horas
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Error storing data in Redis: {str(e)}")

    return weather_data
