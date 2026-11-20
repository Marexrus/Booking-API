from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Booking API"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///app/database/bookings.db"

settings = Settings()