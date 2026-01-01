from fastapi import APIRouter, HTTPException, Header
import httpx
from app.core.config import settings

router = APIRouter()


@router.get("/{track_id}")
async def get_track(track_id: str, authorization: str = Header(...)):
    """トラック情報取得"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.SPOTIFY_API_BASE_URL}/tracks/{track_id}",
                headers={"Authorization": authorization},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=f"トラック情報の取得に失敗しました: {str(e)}"
            )
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"トラック情報の取得に失敗しました: {str(e)}")


@router.get("/{track_id}/features")
async def get_audio_features(track_id: str, authorization: str = Header(...)):
    """Audio Features取得"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.SPOTIFY_API_BASE_URL}/audio-features/{track_id}",
                headers={"Authorization": authorization},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"オーディオ特徴の取得に失敗しました: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"オーディオ特徴の取得に失敗しました: {str(e)}")
