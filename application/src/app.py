from fastapi import FastAPI

from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from api.auth_api import auth_router
from api.job_api import job_router
from errors.exception_handler import register_exception_handler

load_dotenv()

def create_app()->FastAPI:
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(job_router)
    register_exception_handler(app)
    return app

app = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def check_health():
    return {"health":"Pass"}



