from application.services import FinishWalkingService
from fastapi import APIRouter, HTTPException
from infrastructure.persistence.repository import TrajectoryRepository
from pydantic import BaseModel


class FinishWalkingRequest(BaseModel):
    trajectoryId: str


class FinishWalkingResponse(BaseModel):
    trajectoryId: str


router = APIRouter()

finish_walking_service = FinishWalkingService(trajectory_repo=TrajectoryRepository())


@router.post(
    "/api/walking/finish",
    response_model=FinishWalkingRequest,
    status_code=201,
)
async def finish_walking(
    request: FinishWalkingRequest,
) -> FinishWalkingResponse:
    """歩行者が歩行を終了することをサーバに通知するためのエンドポイント."""
    try:
        finish_walking_service.run(trajectory_id=request.trajectoryId)

        return FinishWalkingResponse(trajectoryId=request.trajectoryId)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e
