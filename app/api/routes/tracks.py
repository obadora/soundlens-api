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
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=response.status_code if hasattr(response, 'status_code') else 500,
                detail=f"Failed to fetch track: {str(e)}"
            )


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
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=response.status_code if hasattr(response, 'status_code') else 500,
                detail=f"Failed to fetch audio features: {str(e)}"
            )