# Swagger UI でのトラック情報取得APIの動作確認方法

## 事前準備

1. **Dockerコンテナを起動**
   ```bash
   docker-compose up
   ```

2. **Swagger UIにアクセス**

   ブラウザで以下のURLを開く：
   ```
   http://localhost:8000/docs
   ```

## 認証トークンの取得

トラック情報取得APIを使用する前に、Spotify認証を行いアクセストークンを取得する必要があります。

### ステップ1: ログインURLを取得

1. Swagger UIで`GET /auth/login`エンドポイントを探す
2. 「Try it out」をクリック
3. 「Execute」をクリック
4. レスポンスの`auth_url`をコピー

### ステップ2: Spotifyで認証

1. コピーした`auth_url`をブラウザの新しいタブで開く
2. Spotifyにログインし、アプリケーションを認可
3. リダイレクト後、URLに含まれる`code`パラメータをコピー
   ```
   http://localhost:3000/callback?code=XXXXXXXXXX
   ```

### ステップ3: 認証コードをトークンに交換

1. Swagger UIで`POST /auth/callback`エンドポイントを探す
2. 「Try it out」をクリック
3. Request bodyに以下を入力：
   ```json
   {
     "code": "ステップ2でコピーした認証コード"
   }
   ```
4. 「Execute」をクリック
5. レスポンスの`access_token`をコピー（これを後で使用）

## トラック情報取得APIの使用方法

### 方法1: トラック基本情報の取得

`GET /api/tracks/{track_id}`エンドポイントを使用します。

#### 手順

1. Swagger UIで`GET /api/tracks/{track_id}`を探す
2. 「Try it out」をクリック
3. パラメータを入力：
   - **track_id**: SpotifyのトラックID（例: `11dFghVXANMlKmJXsNCbNl`）
   - **authorization**: `Bearer <アクセストークン>`

     例: `Bearer BQC...xyz`

4. 「Execute」をクリック

#### レスポンス例

```json
{
  "id": "11dFghVXANMlKmJXsNCbNl",
  "name": "Cut To The Feeling",
  "artists": [
    {
      "id": "6sFIWsNpZYqfjUpaCgueju",
      "name": "Carly Rae Jepsen"
    }
  ],
  "album": {
    "id": "1DFixLWuPkv3KT3TnV35m3",
    "name": "Cut To The Feeling",
    "release_date": "2017-05-26"
  },
  "duration_ms": 207959,
  "popularity": 63
}
```

### 方法2: オーディオ特徴の取得

`GET /api/tracks/{track_id}/features`エンドポイントを使用します。

#### 手順

1. Swagger UIで`GET /api/tracks/{track_id}/features`を探す
2. 「Try it out」をクリック
3. パラメータを入力：
   - **track_id**: SpotifyのトラックID
   - **authorization**: `Bearer <アクセストークン>`

4. 「Execute」をクリック

#### レスポンス例

```json
{
  "id": "11dFghVXANMlKmJXsNCbNl",
  "danceability": 0.835,
  "energy": 0.859,
  "key": 1,
  "loudness": -3.813,
  "mode": 1,
  "speechiness": 0.0328,
  "acousticness": 0.0177,
  "instrumentalness": 0.000389,
  "liveness": 0.0797,
  "valence": 0.548,
  "tempo": 125.993,
  "duration_ms": 207960,
  "time_signature": 4
}
```

## SpotifyトラックIDの見つけ方

### Spotifyアプリから

1. Spotifyで任意の曲を探す
2. 曲を右クリック → 「共有」→ 「曲のリンクをコピー」
3. リンク形式：`https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl`
4. `/track/`の後の文字列がトラックID

### Spotify Web Playerから

1. https://open.spotify.com で曲を再生
2. URLからトラックIDを取得
   ```
   https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl
                                  ↑
                            これがトラックID
   ```

## エラーハンドリング

### よくあるエラー

1. **422 Unprocessable Entity**
   - 原因: `authorization`ヘッダーが欠けている
   - 解決: Authorizationヘッダーを正しく設定

2. **401 Unauthorized**
   - 原因: アクセストークンが無効または期限切れ
   - 解決: 新しいアクセストークンを取得

3. **404 Not Found**
   - 原因: トラックIDが存在しない
   - 解決: 正しいトラックIDを使用

4. **500 Internal Server Error**
   - 原因: ネットワークエラーまたはSpotify API側の問題
   - エラーメッセージ: 「トラック情報の取得に失敗しました」または「オーディオ特徴の取得に失敗しました」

## Tips

- アクセストークンは1時間で期限切れになります
- 期限切れの場合は再度認証フローを実行してください
- Swagger UIの「Authorize」ボタン（🔓アイコン）を使用すると、全てのエンドポイントに自動的にAuthorizationヘッダーを設定できます（現在の実装では手動入力が必要）

## 次のステップ

実際のアプリケーションでは、以下の改善が推奨されます：

1. リフレッシュトークンを使用した自動トークン更新
2. トークンの安全な保存（セッション、Cookie、ローカルストレージ）
3. レスポンスキャッシュによるAPI呼び出し削減
4. エラーハンドリングの強化
