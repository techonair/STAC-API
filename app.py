import uvicorn
from fastapi import FastAPI
from stac_api.middleware import setup_middlewares
from stac_app.routes import router
from stac_api.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.enable_swagger else None,
    redoc_url="/redoc" if settings.enable_swagger else None,
)

setup_middlewares(app)

app.include_router(router)

def run():
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the STAC API service!"}