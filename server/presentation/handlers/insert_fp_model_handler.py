from typing import Annotated

from application.services import InsertFpModelService
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel


class InsertFpModelResponse(BaseModel):
    status: str


router = APIRouter()

insert_fp_model_service = InsertFpModelService()


@router.post(
    "/api/buildings/{building_id}/floors/{floor_id}/coordinates/{x}/{y}",
    status_code=201,
)
async def insert_fp_model(
    building_id: str,
    floor_id: str,
    x: int,
    y: int,
    fp_model_file: Annotated[UploadFile, File()],
) -> InsertFpModelResponse:
    """指定された座標に指紋データを登録するためのエンドポイント."""
    _ = insert_fp_model_service.run(
        building_id=building_id,
        floor_id=floor_id,
        x=x,
        y=y,
        fp_model_file=await fp_model_file.read(),
    )
    return InsertFpModelResponse(status="success")
