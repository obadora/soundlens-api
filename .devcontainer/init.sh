#!/bin/bash

# devcontainer初期化スクリプト
# 1. 既存のコンテナを削除
# 2. メインworktreeから.envをコピー

set -e

WORKSPACE_DIR="$1"

# 既存のコンテナを削除
echo "既存のコンテナを削除中..."
docker-compose -f "${WORKSPACE_DIR}/docker-compose.yml" down --remove-orphans 2>/dev/null || true

# ポート8000を使用している他のコンテナも停止
echo "ポート8000を使用しているコンテナをチェック中..."
CONTAINERS_USING_8000=$(docker ps --filter "publish=8000" --format "{{.Names}}" 2>/dev/null || echo "")
if [ -n "$CONTAINERS_USING_8000" ]; then
    echo "ポート8000を使用しているコンテナを停止中: $CONTAINERS_USING_8000"
    echo "$CONTAINERS_USING_8000" | xargs -r docker stop
    echo "$CONTAINERS_USING_8000" | xargs -r docker rm
fi

# メインworktreeから.envをコピー
echo ".envファイルをチェック中..."
if [ ! -f "${WORKSPACE_DIR}/.env" ]; then
    # メインworktreeのパスを取得
    MAIN_WORKTREE=$(git -C "${WORKSPACE_DIR}" worktree list 2>/dev/null | head -n 1 | awk '{print $1}' || echo "")

    if [ -n "$MAIN_WORKTREE" ] && [ -f "$MAIN_WORKTREE/.env" ]; then
        cp "$MAIN_WORKTREE/.env" "${WORKSPACE_DIR}/.env"
        echo "✓ .envをコピーしました: $MAIN_WORKTREE/.env -> ${WORKSPACE_DIR}/.env"
    else
        echo "⚠ メインworktreeの.envが見つかりません"
    fi
else
    echo "✓ .envは既に存在します"
fi

echo "初期化完了"
