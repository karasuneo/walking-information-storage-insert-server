from typing import Annotated

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel


class InsertFpModelResponse(BaseModel):
    status: str


router = APIRouter()


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
    print(f"building_id: {building_id}")
    print(f"floor_id: {floor_id}")
    print(f"x: {x}")
    print(f"y: {y}")
    print(f"fp_model_file: {fp_model_file}")

    return InsertFpModelResponse(status="success")
