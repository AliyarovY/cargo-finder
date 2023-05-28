from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    debug: bool = True
    db_url: str

    server_host: str = '127.0.0.1'
    server_port: int = 8000


settings = Settings(
    _env_file=BASE_DIR / '.env',
    _env_file_encoding='utf-8',
)
