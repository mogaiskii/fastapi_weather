__all__ = ['settings', 'app']
from fastapi.middleware.cors import CORSMiddleware

from api.rest.router import rest_app
from app import app
from settings import settings

app.include_router(rest_app, prefix="/rest")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
