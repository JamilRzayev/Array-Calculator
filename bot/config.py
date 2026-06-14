from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    DATABASE_URL: str

    MARZBAN_ADDRESS: str
    MARZBAN_USERNAME: str
    MARZBAN_PASSWORD: str
    MARZBAN_SKIP_SSL_VERIFY: bool = False

    SHOP_ID: str | None = None
    SHOP_SECRET_KEY: str | None = None
    CRYPTO_PAY_TOKEN: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()
