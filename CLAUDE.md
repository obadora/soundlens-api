# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

SoundLens APIは、Spotify APIと連携する音楽分析・比較アプリケーションです。FastAPIをベースとし、認証とトラック情報取得のエンドポイントを提供します。将来的には日本語NLPツール（Janome）とTextBlobを使用した歌詞分析機能を実装予定です。

## アーキテクチャ

### アプリケーション構造

レイヤー化されたFastAPIアーキテクチャを採用しています：

- **`app/main.py`**: アプリケーションのエントリーポイント。FastAPIのセットアップ、CORSミドルウェアの設定、ルーター登録を行う
- **`app/core/config.py`**: pydantic-settingsを使用した一元的な設定管理。`.env`ファイルから設定を読み込む
- **`app/api/routes/`**: APIルートハンドラー
  - `auth.py`: Spotify OAuth フロー（ログインURL生成、トークン交換）
  - `track.py`: Spotifyのトラックデータとオーディオ特徴の取得
- **`app/models/`**: Pydanticモデル（現在は空、モデルはルート内でインライン定義）
- **`app/services/`**: ビジネスロジック層（現在は空）
- **`app/utils/`**: ユーティリティ関数（現在は空）
- **`tests/`**: テストスイート（現在は空）

### 主要な依存関係

- **FastAPI 0.109.0**: コアWebフレームワーク
- **Pydantic 2.5.3**: データ検証と設定管理
- **httpx**: Spotify API呼び出し用の非同期HTTPクライアント
- **Spotify API**: OAuth 2.0認証とトラックデータ取得
- **Janome + TextBlob**: 日本語・英語のテキスト分析（歌詞分析用、将来実装予定）
- **NumPy + Pandas**: データ分析サポート（将来実装予定）

### 設定管理

すべての設定は`app/core/config.py`で`pydantic_settings.BaseSettings`を使用して管理されます：
- Spotify認証情報（CLIENT_ID、CLIENT_SECRET）
- リダイレクトURIと許可されたCORSオリジン
- 環境設定（development/production）
- Spotify APIエンドポイント（auth、token、base URL）

設定値は実行時に`.env`ファイルから読み込まれます。

### 認証フロー

Spotifyの認可コードフローを実装しています：
1. クライアントが`GET /auth/login`経由でログインURLをリクエスト
2. ユーザーがSpotifyで認可し、認可コードと共にリダイレクトされる
3. クライアントが`POST /auth/callback`経由でコードをトークンと交換
4. 以降のAPI呼び出しではAuthorizationヘッダーでアクセストークンを使用

## 開発コマンド

### パッケージ管理（Poetry）

このプロジェクトはPoetryで依存関係を管理しています。ローカルにPoetryをインストールする必要はなく、Docker/Dev Container内で実行できます。

```bash
# パッケージを追加（本番用）
docker-compose exec api poetry add パッケージ名

# パッケージを追加（開発用）
docker-compose exec api poetry add --group dev パッケージ名

# パッケージを削除
docker-compose exec api poetry remove パッケージ名

# 依存関係の確認
docker-compose exec api poetry show

# poetry.lockの更新（依存関係の最新化）
docker-compose exec api poetry update
```

### Docker開発環境（推奨）

```bash
# ホットリロード付きで開発サーバーを起動
docker-compose up

# 依存関係変更後にコンテナを再ビルド
docker-compose up --build

# サービスを停止
docker-compose down

# クリーンビルド（キャッシュを使わない）
docker-compose build --no-cache
```

Docker環境の特徴：
- ポート8000で実行
- ホットリロード用にプロジェクトディレクトリをマウント（`/src`）
- Python 3.11 Slim（Debian系）+ Poetryを使用
- __pycache__と.pytest_cacheはボリュームマウントから除外

### VSCode Dev Container（推奨）

VSCodeでDev Containerを使用すると、コンテナ内で直接開発できます：

1. VSCodeで「Dev Containers」拡張機能をインストール
2. コマンドパレット（Cmd+Shift+P）から「Dev Containers: Reopen in Container」を実行
3. コンテナ内で直接Poetryコマンドが使える

```bash
# Dev Container内で
poetry add httpx
poetry install --with dev
```

### テストと品質管理

```bash
# テストを実行
docker-compose exec api pytest

# 特定のテストファイルを実行
docker-compose exec api pytest tests/test_specific.py

# カバレッジ付きでテストを実行
docker-compose exec api pytest --cov=app tests/

# コードをフォーマット
docker-compose exec api black .

# コードをLint
docker-compose exec api flake8 app/

# 型チェック
docker-compose exec api mypy app/
```

### APIドキュメント

サーバー起動中は、インタラクティブなAPIドキュメントが利用可能です：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- ヘルスチェック: http://localhost:8000/health

## 重要な注意事項

### 環境設定

以下の変数を含む`.env`ファイルが必要です：
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:3000/callback
ALLOWED_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

### コーディングスタイル

このプロジェクトでは、コメントとdocstringに日本語を使用しています。新しいコードを追加する際は、一貫性を保つためこの規則に従ってください。

### ルーター登録

新しいルートファイルは`app/main.py`でインポートして登録する必要があります：
```python
from app.api.routes import new_module
app.include_router(new_module.router, prefix="/api/path", tags=["タグ"])
```

### 非同期パターン

すべてのSpotify API呼び出しは、httpx.AsyncClientでasync/awaitを使用しています。新しい外部API統合を行う際も、このパターンを維持してください。

### エラーハンドリング

Spotify APIからのHTTPエラーはキャッチされ、適切なステータスコードと詳細メッセージを含むFastAPIのHTTPExceptionとして再発生させます。
