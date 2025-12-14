"""トラックルートのユニットテスト"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx


class TestGetTrack:
    """トラック情報取得エンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_get_track_success(self, client, sample_track_data):
        """トラック情報の取得が成功することを確認"""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_track_data
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/test_track_id", headers={"Authorization": "Bearer test_access_token"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_track_id"
            assert data["name"] == "Test Track"
            assert data["artists"][0]["name"] == "Test Artist"

            # GETリクエストが正しく呼ばれたことを確認
            mock_client_instance.get.assert_called_once()
            call_args = mock_client_instance.get.call_args
            assert "tracks/test_track_id" in str(call_args)

    def test_get_track_missing_authorization(self, client):
        """認証ヘッダーが欠けている場合にエラーになることを確認"""
        response = client.get("/api/tracks/test_track_id")

        # 422 Unprocessable Entity (バリデーションエラー)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_track_invalid_token(self, client):
        """無効なトークンでエラーになることを確認"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=MagicMock(status_code=401)
        )

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/test_track_id", headers={"Authorization": "Bearer invalid_token"}
            )

            assert response.status_code == 401
            data = response.json()
            assert "detail" in data

    @pytest.mark.asyncio
    async def test_get_track_not_found(self, client):
        """存在しないトラックIDでエラーになることを確認"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=MagicMock(status_code=404)
        )

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/non_existent_track",
                headers={"Authorization": "Bearer test_access_token"},
            )

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_track_network_error(self, client):
        """ネットワークエラーが発生した場合の処理を確認"""
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = httpx.ConnectError("Connection failed")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/test_track_id", headers={"Authorization": "Bearer test_access_token"}
            )

            assert response.status_code == 500
            data = response.json()
            assert "Failed to fetch track" in data["detail"]

    @pytest.mark.asyncio
    async def test_get_track_authorization_header_forwarded(self, client, sample_track_data):
        """認証ヘッダーがSpotify APIに正しく転送されることを確認"""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_track_data
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            test_token = "Bearer test_access_token_123"
            response = client.get(
                "/api/tracks/test_track_id", headers={"Authorization": test_token}
            )

            assert response.status_code == 200

            # GETリクエストの引数を確認
            call_args = mock_client_instance.get.call_args
            headers = call_args.kwargs["headers"]
            assert headers["Authorization"] == test_token


class TestGetAudioFeatures:
    """オーディオ特徴取得エンドポイントのテスト"""

    @pytest.mark.asyncio
    async def test_get_audio_features_success(self, client, sample_audio_features):
        """オーディオ特徴の取得が成功することを確認"""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_audio_features
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/test_track_id/features",
                headers={"Authorization": "Bearer test_access_token"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_track_id"
            assert data["danceability"] == 0.8
            assert data["energy"] == 0.7
            assert data["tempo"] == 120.0

            # GETリクエストが正しく呼ばれたことを確認
            mock_client_instance.get.assert_called_once()
            call_args = mock_client_instance.get.call_args
            assert "audio-features/test_track_id" in str(call_args)

    def test_get_audio_features_missing_authorization(self, client):
        """認証ヘッダーが欠けている場合にエラーになることを確認"""
        response = client.get("/api/tracks/test_track_id/features")

        # 422 Unprocessable Entity (バリデーションエラー)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_audio_features_invalid_token(self, client):
        """無効なトークンでエラーになることを確認"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=MagicMock(status_code=401)
        )

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/test_track_id/features",
                headers={"Authorization": "Bearer invalid_token"},
            )

            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_audio_features_not_found(self, client):
        """存在しないトラックIDでエラーになることを確認"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=MagicMock(status_code=404)
        )

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/non_existent_track/features",
                headers={"Authorization": "Bearer test_access_token"},
            )

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_audio_features_network_error(self, client):
        """ネットワークエラーが発生した場合の処理を確認"""
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = httpx.ConnectError("Connection failed")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            response = client.get(
                "/api/tracks/test_track_id/features",
                headers={"Authorization": "Bearer test_access_token"},
            )

            assert response.status_code == 500
            data = response.json()
            assert "Failed to fetch audio features" in data["detail"]

    @pytest.mark.asyncio
    async def test_get_audio_features_authorization_header_forwarded(
        self, client, sample_audio_features
    ):
        """認証ヘッダーがSpotify APIに正しく転送されることを確認"""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_audio_features
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            test_token = "Bearer test_access_token_456"
            response = client.get(
                "/api/tracks/test_track_id/features", headers={"Authorization": test_token}
            )

            assert response.status_code == 200

            # GETリクエストの引数を確認
            call_args = mock_client_instance.get.call_args
            headers = call_args.kwargs["headers"]
            assert headers["Authorization"] == test_token
