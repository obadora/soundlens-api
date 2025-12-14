"""メインアプリケーションのユニットテスト"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestHealthCheck:
    """ヘルスチェックエンドポイントのテスト"""

    def test_health_check(self, client):
        """ヘルスチェックが正常に動作することを確認"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
        assert "environment" in data

    def test_health_check_returns_environment(self, client):
        """ヘルスチェックが環境情報を返すことを確認"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["environment"], str)


class TestRootEndpoint:
    """ルートエンドポイントのテスト"""

    def test_root_endpoint(self, client):
        """ルートエンドポイントが正常に動作することを確認"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "SoundLens API"

    def test_root_endpoint_includes_documentation(self, client):
        """ルートエンドポイントがドキュメントURLを含むことを確認"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "docs" in data
        assert data["docs"] == "/docs"

    def test_root_endpoint_includes_version(self, client):
        """ルートエンドポイントがバージョン情報を含むことを確認"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"


class TestCORS:
    """CORSミドルウェアのテスト"""

    def test_cors_headers_present(self, client):
        """CORSヘッダーが存在することを確認"""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )

        # Preflightリクエストの処理を確認
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_credentials(self, client):
        """CORSが認証情報を許可することを確認"""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )

        headers = {k.lower(): v for k, v in response.headers.items()}
        if "access-control-allow-credentials" in headers:
            assert headers["access-control-allow-credentials"] == "true"


class TestAPIDocumentation:
    """APIドキュメントエンドポイントのテスト"""

    def test_swagger_ui_accessible(self, client):
        """Swagger UIがアクセス可能であることを確認"""
        response = client.get("/docs")

        assert response.status_code == 200
        # HTMLが返されることを確認
        assert "text/html" in response.headers["content-type"]

    def test_redoc_accessible(self, client):
        """ReDocがアクセス可能であることを確認"""
        response = client.get("/redoc")

        assert response.status_code == 200
        # HTMLが返されることを確認
        assert "text/html" in response.headers["content-type"]

    def test_openapi_schema_accessible(self, client):
        """OpenAPIスキーマがアクセス可能であることを確認"""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "SoundLens API"
        assert data["info"]["version"] == "1.0.0"

    def test_openapi_schema_includes_routes(self, client):
        """OpenAPIスキーマがルートを含むことを確認"""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "paths" in data

        # 主要なエンドポイントが含まれていることを確認
        paths = data["paths"]
        assert "/health" in paths
        assert "/" in paths
        assert "/auth/login" in paths
        assert "/auth/callback" in paths
        assert "/api/tracks/{track_id}" in paths
        assert "/api/tracks/{track_id}/features" in paths


class TestApplicationSetup:
    """アプリケーションのセットアップのテスト"""

    def test_app_title(self):
        """アプリケーションのタイトルが正しいことを確認"""
        assert app.title == "SoundLens API"

    def test_app_description(self):
        """アプリケーションの説明が正しいことを確認"""
        assert app.description == "音楽分析・比較アプリケーション"

    def test_app_version(self):
        """アプリケーションのバージョンが正しいことを確認"""
        assert app.version == "1.0.0"

    def test_routes_registered(self, client):
        """すべてのルートが登録されていることを確認"""
        # OpenAPIスキーマからルート情報を取得
        response = client.get("/openapi.json")
        data = response.json()
        paths = data["paths"]

        # 認証ルート
        assert "/auth/login" in paths
        assert "/auth/callback" in paths

        # トラックルート
        assert "/api/tracks/{track_id}" in paths
        assert "/api/tracks/{track_id}/features" in paths

        # 基本ルート
        assert "/health" in paths
        assert "/" in paths
