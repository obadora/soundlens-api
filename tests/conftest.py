"""テスト用の共通フィクスチャ"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings


@pytest.fixture
def client():
    """FastAPIテストクライアント"""
    return TestClient(app)


@pytest.fixture
def mock_settings(monkeypatch):
    """モック設定"""
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_ID", "test_client_id")
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_SECRET", "test_client_secret")
    monkeypatch.setattr(settings, "REDIRECT_URI", "http://localhost:3000/callback")
    monkeypatch.setattr(settings, "ALLOWED_ORIGINS", "http://localhost:3000")
    monkeypatch.setattr(settings, "ENVIRONMENT", "test")
    monkeypatch.setattr(settings, "SPOTIFY_AUTH_URL", "https://accounts.spotify.com/authorize")
    monkeypatch.setattr(settings, "SPOTIFY_TOKEN_URL", "https://accounts.spotify.com/api/token")
    monkeypatch.setattr(settings, "SPOTIFY_API_BASE_URL", "https://api.spotify.com/v1")
    return settings


@pytest.fixture
def sample_token_response():
    """サンプルトークンレスポンス"""
    return {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer",
        "scope": "user-read-private user-read-email",
    }


@pytest.fixture
def sample_track_data():
    """サンプルトラックデータ"""
    return {
        "id": "test_track_id",
        "name": "Test Track",
        "artists": [{"id": "test_artist_id", "name": "Test Artist"}],
        "album": {"id": "test_album_id", "name": "Test Album", "release_date": "2024-01-01"},
        "duration_ms": 180000,
        "popularity": 75,
    }


@pytest.fixture
def sample_audio_features():
    """サンプルオーディオ特徴データ"""
    return {
        "id": "test_track_id",
        "danceability": 0.8,
        "energy": 0.7,
        "key": 5,
        "loudness": -5.0,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.1,
        "instrumentalness": 0.0,
        "liveness": 0.2,
        "valence": 0.6,
        "tempo": 120.0,
        "duration_ms": 180000,
        "time_signature": 4,
    }
