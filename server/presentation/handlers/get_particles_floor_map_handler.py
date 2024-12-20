from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

image_path = "particle_floor_map.png"


@router.get(
    "/api/floor_map/get",
    status_code=200,
)
async def get_particles_floor_map() -> FileResponse:
    try:
        if not Path(image_path).exists():
            raise HTTPException(
                status_code=404,
                detail="Image file not found",
            )

        return FileResponse(
            image_path,
            media_type="image/png",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e
