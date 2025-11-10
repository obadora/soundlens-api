from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import base64
from app.core.config import settings

router = APIRouter()


class TokenRequest(BaseModel):
    """トークン交換リクエスト"""
    code: str


class TokenResponse(BaseModel):
    """トークンレスポンス"""
    access_token: str
    refresh_token: str
    expires_in: int


@router.get("/login")
async def get_login_url():
    """Spotify認証URL生成"""
    scopes = [
        "user-read-private",
        "user-read-email",
        "user-top-read",
        "user-read-recently-played",
    ]
    
    auth_url = (
        f"{settings.SPOTIFY_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={settings.SPOTIFY_CLIENT_ID}"
        f"&scope={' '.join(scopes)}"
        f"&redirect_uri={settings.REDIRECT_URI}"
    )
    
    return {"auth_url": auth_url}


@router.post("/callback", response_model=TokenResponse)
async def exchange_token(request: TokenRequest):
    """認証コードをアクセストークンに交換"""
    
    # Basic認証用のエンコード
    credentials = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": request.code,
        "redirect_uri": settings.REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.SPOTIFY_TOKEN_URL,
                headers=headers,
                data=data,
            )
            response.raise_for_status()
            token_data = response.json()
            
            return TokenResponse(
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                expires_in=token_data["expires_in"],
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to exchange token: {str(e)}"
            )