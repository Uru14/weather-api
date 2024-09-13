from fastapi import FastAPI

app = FastAPI()

@app.get("/weather")
async def get_weather():
    return {"message": "Hello, this is the weather API"}