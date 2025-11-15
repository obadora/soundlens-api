# 開発環境用 Dockerfile (FastAPI)
FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /usr/src/app

# システム依存関係のインストール（ビルドに必要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt をコピー
COPY requirements.txt .

# Python依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# ポート公開
EXPOSE 8000

# 開発サーバー起動（ホットリロード対応）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]