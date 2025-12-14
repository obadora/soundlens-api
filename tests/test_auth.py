"""認証ルートのユニットテスト"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from app.core.config import settings


class TestAuthLogin:
    """ログインエンドポイントのテスト"""

    def test_get_login_url_success(self, client):
        """ログインURL生成が成功することを確認"""
        response = client.get("/auth/login")

        assert response.status_code == 200
        data = response.json()
        assert "auth_url" in data

        # URLに必要なパラメータが含まれていることを確認
        auth_url = data["auth_url"]
        assert settings.SPOTIFY_AUTH_URL in auth_url
        assert f"client_id={settings.SPOTIFY_CLIENT_ID}" in auth_url
        assert "response_type=code" in auth_url
        assert f"redirect_uri={settings.REDIRECT_URI}" in auth_url

        # スコープが含まれていることを確認
        assert "user-read-private" in auth_url
        assert "user-read-email" in auth_url
        assert "user-top-read" in auth_url
        assert "user-read-recently-played" in auth_url


class TestAuthCallback:
    """コールバックエンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_exchange_token_success(self, client, sample_token_response):
        """トークン交換が成功することを確認"""
        # httpx.AsyncClientのモック
        mock_response = MagicMock()
        mock_response.json.return_value = sample_token_response
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.post("/auth/callback", json={"code": "test_auth_code"})

            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "test_access_token"
            assert data["refresh_token"] == "test_refresh_token"
            assert data["expires_in"] == 3600

            # POSTリクエストが正しく呼ばれたことを確認
            mock_client_instance.post.assert_called_once()
            call_args = mock_client_instance.post.call_args
            assert settings.SPOTIFY_TOKEN_URL in str(call_args)

    @pytest.mark.asyncio
    async def test_exchange_token_invalid_code(self, client):
        """無効な認証コードでトークン交換が失敗することを確認"""
        # HTTPエラーをシミュレート
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Invalid authorization code", request=MagicMock(), response=MagicMock(status_code=400)
        )

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.post("/auth/callback", json={"code": "invalid_code"})

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Failed to exchange token" in data["detail"]

    def test_exchange_token_missing_code(self, client):
        """認証コードが欠けている場合にエラーになることを確認"""
        response = client.post("/auth/callback", json={})

        # Pydanticのバリデーションエラー
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_exchange_token_network_error(self, client):
        """ネットワークエラーが発生した場合の処理を確認"""
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = httpx.ConnectError("Connection failed")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.post("/auth/callback", json={"code": "test_code"})

            assert response.status_code == 500
            data = response.json()
            assert "Failed to exchange token" in data["detail"]

    @pytest.mark.asyncio
    async def test_exchange_token_authorization_header(self, client, sample_token_response):
        """Basic認証ヘッダーが正しく生成されることを確認"""
        import base64

        mock_response = MagicMock()
        mock_response.json.return_value = sample_token_response
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.post("/auth/callback", json={"code": "test_auth_code"})

            assert response.status_code == 200

            # POSTリクエストの引数を確認
            call_args = mock_client_instance.post.call_args
            headers = call_args.kwargs["headers"]

            # Basic認証ヘッダーが存在することを確認
            assert "Authorization" in headers
            assert headers["Authorization"].startswith("Basic ")

            # エンコードされた認証情報を確認
            encoded = headers["Authorization"].replace("Basic ", "")
            decoded = base64.b64decode(encoded).decode()
            assert settings.SPOTIFY_CLIENT_ID in decoded
            assert settings.SPOTIFY_CLIENT_SECRET in decoded
