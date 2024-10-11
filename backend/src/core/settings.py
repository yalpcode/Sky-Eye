from pydantic import Field
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    APP_TITLE: str = Field('Drone AI API')
    APP_DEBUG: bool = Field(False)
    APP_BASE_URL: str = Field('http://localhost:8000')
    APP_AUTH_TOKEN: str = Field("*")


application_settings = ApplicationSettings()
