from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = ''

    debug: bool = False

    def get_db_url(self):
        return self.db_url


settings = Settings()
