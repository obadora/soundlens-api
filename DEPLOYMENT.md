# SoundLens API デプロイメントガイド

このガイドでは、Render + Supabaseを使用してSoundLens APIを無料でデプロイする手順を説明します。

## 前提条件

- GitHubアカウント
- Renderアカウント（無料）
- Supabaseアカウント（無料）
- Spotifyアプリケーションの認証情報（CLIENT_ID、CLIENT_SECRET）

---

## 1. Supabase（PostgreSQL）のセットアップ

### 1.1 Supabaseプロジェクトの作成

1. [Supabase](https://supabase.com/)にアクセスしてログイン
2. 「New Project」をクリック
3. プロジェクト情報を入力：
   - **Name**: `soundlens-db` (任意)
   - **Database Password**: 強固なパスワードを設定（保存しておく）
   - **Region**: Singapore（日本に近いリージョン）
   - **Pricing Plan**: Free
4. 「Create new project」をクリック（セットアップに数分かかります）

### 1.2 データベース接続文字列の取得

1. プロジェクトダッシュボードで「Settings」→「Database」に移動
2. 「Connection string」セクションで「URI」を選択
3. **Connection pooling**を使用する場合（推奨）：
   - 「Connection Pooling」タブに切り替え
   - 「Transaction Mode」を選択
   - 接続文字列をコピー（形式: `postgresql://postgres.xxxxx:password@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres`）
4. `[YOUR-PASSWORD]`の部分を実際のパスワードに置き換える
5. この接続文字列を後でRenderで使用するため保存しておく

**注意**:
- Supabaseの無料プランは2週間非アクティブで一時停止しますが、アクセスすれば即座に復帰します
- 現時点ではDBを使用していませんが、将来的な拡張のために設定しておきます

---

## 2. Render（FastAPI）のセットアップ

### 2.1 GitHubリポジトリの準備

1. このプロジェクトをGitHubにプッシュ
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

### 2.2 Renderでサービスを作成

1. [Render](https://render.com/)にアクセスしてログイン
2. ダッシュボードで「New +」→「Web Service」をクリック
3. GitHubリポジトリを接続：
   - 「Connect a repository」で該当リポジトリを選択
   - 「Connect」をクリック

### 2.3 サービス設定

Renderは`render.yaml`を自動的に検出しますが、以下を確認：

- **Name**: `soundlens-api`（自動設定済み）
- **Region**: Singapore（自動設定済み）
- **Branch**: `main`（デプロイするブランチ）
- **Runtime**: Docker（自動検出）
- **Plan**: Free

### 2.4 環境変数の設定

「Environment」タブで以下の環境変数を追加：

#### 必須の環境変数

| キー | 値 | 説明 |
|------|-----|------|
| `SPOTIFY_CLIENT_ID` | `your_spotify_client_id` | Spotify APIのクライアントID |
| `SPOTIFY_CLIENT_SECRET` | `your_spotify_client_secret` | Spotify APIのクライアントシークレット |
| `REDIRECT_URI` | `https://your-frontend-domain/callback` | フロントエンドのコールバックURL |
| `ALLOWED_ORIGINS` | `https://your-frontend-domain` | CORSで許可するオリジン（複数の場合はカンマ区切り） |
| `DATABASE_URL` | `postgresql://postgres.xxxxx...` | Supabaseの接続文字列（手順1.2で取得） |
| `ENVIRONMENT` | `production` | 環境設定（自動設定済み） |
| `DEBUG` | `false` | デバッグモード（自動設定済み） |

#### Spotify認証情報の取得方法

1. [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)にアクセス
2. 「Create app」で新しいアプリを作成
3. アプリの設定で以下を確認：
   - **Redirect URIs**: `https://your-frontend-domain/callback`を追加
   - **Client ID**と**Client Secret**をコピーして環境変数に設定

### 2.5 デプロイの実行

1. すべての環境変数を設定したら「Create Web Service」をクリック
2. 初回デプロイが自動的に開始されます（5〜10分程度）
3. ビルドログで進捗を確認

### 2.6 デプロイ確認

デプロイが完了したら、RenderのダッシュボードでサービスURLを確認：

```
https://soundlens-api.onrender.com
```

以下のエンドポイントにアクセスして動作確認：

- **ルート**: `https://soundlens-api.onrender.com/`
- **ヘルスチェック**: `https://soundlens-api.onrender.com/health`
- **API ドキュメント**: `https://soundlens-api.onrender.com/docs`

---

## 3. 継続的デプロイ（CD）の設定

Renderは自動的にGitHub連携で継続的デプロイを設定します：

- `main`ブランチへのプッシュで自動的に再デプロイ
- Pull Requestのプレビュー環境も作成可能（有料プランで利用可能）

### 手動デプロイ

必要に応じて、Renderダッシュボードから「Manual Deploy」→「Deploy latest commit」で手動デプロイも可能です。

---

## 4. トラブルシューティング

### デプロイが失敗する場合

1. **ビルドログを確認**：
   - Renderダッシュボードの「Logs」タブでエラーメッセージを確認
   - Dockerfileの構文エラーや依存関係の問題がないか確認

2. **環境変数の確認**：
   - すべての必須環境変数が設定されているか確認
   - 値に余分なスペースや引用符がないか確認

3. **ヘルスチェックの失敗**：
   - `/health`エンドポイントが正しく動作しているか確認
   - `app/main.py:28-34`のヘルスチェックハンドラーを確認

### アプリケーションが起動しない場合

1. **ログを確認**：
   ```bash
   # Renderダッシュボードの「Logs」タブで確認
   ```

2. **ローカルで同じ設定をテスト**：
   ```bash
   # Dockerで本番環境をシミュレート
   docker build -t soundlens-api .
   docker run -p 8000:8000 --env-file .env soundlens-api \
     uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### データベース接続の問題

1. **接続文字列の確認**：
   - Supabaseの接続文字列が正しいか確認
   - パスワードが正しく設定されているか確認

2. **Supabaseのステータス確認**：
   - Supabaseダッシュボードでプロジェクトが稼働中か確認
   - 2週間非アクティブで一時停止している場合は再起動

### 無料プランの制限

**Render Free Tier制限**：
- 無操作時に自動スリープ（初回リクエストで自動起動、数秒かかる）
- 月750時間の稼働時間（実質常時稼働可能）
- メモリ512MB

**Supabase Free Tier制限**：
- 500MBストレージ
- 2週間非アクティブで一時停止（再起動可能）
- 月5GBの帯域幅

---

## 5. 将来の拡張

### データベースマイグレーション

データベーススキーマを管理する場合、Alembicを使用：

```bash
# マイグレーション初期化
docker-compose exec api alembic init alembic

# マイグレーションファイル作成
docker-compose exec api alembic revision --autogenerate -m "Initial migration"

# マイグレーション実行
docker-compose exec api alembic upgrade head
```

### Renderでのマイグレーション実行

1. Renderダッシュボードで「Shell」タブを開く
2. 以下のコマンドを実行：
   ```bash
   alembic upgrade head
   ```

または、デプロイ時に自動実行する場合は`render.yaml`に追加：
```yaml
services:
  - type: web
    name: soundlens-api
    # ...
    buildCommand: poetry install --only main && alembic upgrade head
```

---

## 6. 環境変数のサンプル（.env）

ローカル開発用の`.env`サンプル：

```env
# Spotify API
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:3000/callback
ALLOWED_ORIGINS=http://localhost:3000

# Application
ENVIRONMENT=development
DEBUG=true

# Database (optional for local development)
DATABASE_URL=postgresql://user:password@localhost:5432/soundlens
```

---

## 7. 参考リンク

- [Render Documentation](https://render.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)

---

## 完了

これで、SoundLens APIがRender + Supabaseで完全無料でデプロイされました！
