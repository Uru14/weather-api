from fastapi import FastAPI
from app.routers import weather
from app.settings import settings

app = FastAPI()

app.include_router(weather.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
