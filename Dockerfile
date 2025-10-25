# 開発環境用 Dockerfile
FROM node:20-alpine

# 開発に必要なツールをインストール
RUN apk add --no-cache git

# 作業ディレクトリ設定
WORKDIR /usr/src/app

# package.json と package-lock.json をコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー（Dev Containerではマウントで上書きされる）
COPY . .

# ポート公開
EXPOSE 3000 9229