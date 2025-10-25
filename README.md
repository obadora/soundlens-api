# SoundLens API

Spotify API を使った音楽分析バックエンド

## Dev Container で開発する

### 必要なもの

- Docker Desktop
- VSCode
- VSCode拡張機能: [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### セットアップ手順

1. **VSCodeでプロジェクトを開く**

2. **Dev Containerで開き直す**
   - `Cmd + Shift + P` (Mac) / `Ctrl + Shift + P` (Windows)
   - `Dev Containers: Reopen in Container` を選択
   - 初回は Docker イメージのビルドに数分かかります

3. **開発サーバーを起動**
   ```bash
   npm run dev
   ```

4. **ブラウザでアクセス**
   - http://localhost:3000/

### Dev Container の機能

- コンテナ内のターミナルで直接 `npm` コマンドが使える
- TypeScript IntelliSense が正確に動作
- ファイル保存時に自動フォーマット（Prettier）
- Git 操作もコンテナ内で可能

### 通常の Docker で開発する場合

Dev Container を使わない場合:

```bash
# コンテナ起動
docker-compose up -d

# ログ確認
docker-compose logs -f

# コンテナ停止
docker-compose down
```

## API エンドポイント

- `GET /` - API情報
- `GET /health` - ヘルスチェック

## 環境変数

`.env` ファイルで設定:

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:5173/callback
PORT=3000
NODE_ENV=development
```
