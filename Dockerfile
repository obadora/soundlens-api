# 開発環境用 Dockerfile (FastAPI + Poetry)
FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /src

# システム依存関係のインストール（ビルドに必要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

# pyproject.tomlとpoetry.lockをコピー（依存関係定義）
COPY pyproject.toml poetry.lock* ./

# 依存関係のインストール（本番用のみ、開発用は除外）
RUN poetry install --no-root --only main

# ソースコードをコピー
COPY . .

# アプリケーションをインストール（--no-devで開発依存関係は除外）
RUN poetry install --only-root

# ポート公開
EXPOSE 8000

# 開発サーバー起動（ホットリロード対応）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]