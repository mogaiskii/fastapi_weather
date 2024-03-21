__all__ = ['settings', 'app']

from api.rest.router import rest_app
from app import app
from settings import settings

app.include_router(rest_app, prefix="/rest")
