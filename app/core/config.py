from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """アプリケーション設定"""

    # Spotify API
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    REDIRECT_URI: str = "http://127.0.0.1:3000/callback"

    # アプリケーション設定
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: str = "http://127.0.0.1:3000"

    # Spotify API エンドポイント
    SPOTIFY_AUTH_URL: str = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL: str = "https://api.spotify.com/v1"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # 余分な環境変数を無視
    )


settings = Settings()
