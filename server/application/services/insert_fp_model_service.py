from application.dto.application_dto import InsertFpModelDto
from config.const import HEALTH_CHECK_BUCKET_NAME
from infrastructure.connection import DBConnection, MinIOConnection
from infrastructure.external.services import FileService
from infrastructure.persistence.repository import CoordinateRepository, WifiFingerPrintingRepository


class InsertFpModelService:
    def __init__(
        self,
    ) -> None:
        pass

    def run(
        self,
        building_id: str,
        floor_id: str,
        x: int,
        y: int,
        fp_model_file: bytes,
    ) -> InsertFpModelDto:
        conn = DBConnection.connect()
        s3 = MinIOConnection.connect()
        file_service = FileService(s3)

        coordinate_repo = CoordinateRepository()
        wifi_fingerprinting_repo = WifiFingerPrintingRepository()

        coordinate_repo_dto = coordinate_repo.find_for_coordinate(conn=conn, x=x, y=y)
        _ = wifi_fingerprinting_repo.save(
            conn=conn, coordinate_id=coordinate_repo_dto.id
        )

        file_service.upload(
            key=f"{HEALTH_CHECK_BUCKET_NAME}/{building_id}/{floor_id}/{x}/{y}",
            file=fp_model_file,
        )

        return InsertFpModelDto(
            building_id=building_id,
            floor_id=floor_id,
            x=x,
            y=y,
            fp_model_file=fp_model_file,
        )
