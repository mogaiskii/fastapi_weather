from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    version: str = ''
    DEFAULT_LAT: float = "44.8125"
    DEFAULT_LON: float = "20.4612"
    DEFAULT_TZ: str = "Europe/Belgrade"


try:
    with open(".version") as f:
        version = f.read()
except Exception:
    version = 'NA'

settings = Settings(version=version)
