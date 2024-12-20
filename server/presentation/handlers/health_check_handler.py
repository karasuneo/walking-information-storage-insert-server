from io import BytesIO
from typing import Annotated

from application.services import HealthCheckService
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

health_check_service = HealthCheckService()

router = APIRouter()


@router.post(
    "/api/health/minio/csv",
    status_code=201,
)
async def check_minio_csv_health(
    bucketName: Annotated[
        str,
        Form(),
    ],
    uploadFile: Annotated[
        UploadFile,
        File(),
    ],
) -> StreamingResponse:
    """MinIOサーバへのファイルアップロード及びダウンロードが正常に行えるかを確認するためのエンドポイント."""
    try:
        upload_file = await uploadFile.read()

        download_file = health_check_service.minio(
            bucket_name=bucketName,
            upload_file=upload_file,
        )

        return StreamingResponse(
            content=BytesIO(download_file),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=download.csv"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e


@router.post(
    "/api/health/minio/img",
    status_code=201,
)
async def check_minio_image_health(
    bucketName: Annotated[
        str,
        Form(),
    ],
    uploadFile: Annotated[
        UploadFile,
        File(),
    ],
) -> StreamingResponse:
    """MinIOサーバへのファイルアップロード及びダウンロードが正常に行えるかを確認するためのエンドポイント."""
    try:
        upload_file = await uploadFile.read()

        download_file = health_check_service.minio(
            bucket_name=bucketName,
            upload_file=upload_file,
        )

        return StreamingResponse(
            content=BytesIO(download_file),
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=image.png"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e
