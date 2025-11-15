from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, tracks

app = FastAPI(
    title="SoundLens API",
    description="音楽分析・比較アプリケーション",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router, prefix="/auth", tags=["認証"])
app.include_router(tracks.router, prefix="/api/tracks", tags=["トラック"])


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "SoundLens API",
        "docs": "/docs",
        "version": "1.0.0",
    }