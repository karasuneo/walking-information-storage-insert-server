from enum import Enum

from fastapi import HTTPException


class InfrastructureErrorType(Enum):
    NOT_FOUND_FLOOR_INFORMATION = "NOT_FOUND_FLOOR_INFORMATION"
    NOT_FOUND_FLOOR_MAP = "NOT_FOUND_FLOOR_MAP"
    NOT_FOUND_FLOOR = "NOT_FOUND_FLOOR"
    NOT_FOUND_TRAJECTORY = "NOT_FOUND_TRAJECTORY"
    NOT_FOUND_WALKING_SAMPLE = "NOT_FOUND_WALKING_SAMPLE"
    BUILDING_DB_ERROR = "BUILDING_DB_ERROR"
    FLOOR_DB_ERROR = "FLOOR_DB_ERROR"
    FLOOR_INFORMATION_DB_ERROR = "FLOOR_INFORMATION_DB_ERROR"
    FLOOR_MAP_DB_ERROR = "FLOOR_MAP_DB_ERROR"
    TRAJECTORY_DB_ERROR = "TRAJECTORY_DB_ERROR"
    WALKING_SAMPLE_DB_ERROR = "WALKING_SAMPLE_DB_ERROR"
    PEDESTRIAN_DB_ERROR = "PEDESTRIAN_DB_ERROR"
    WALKING_INFORMATION_DB_ERROR = "WALKING_INFORMATION_DB_ERROR"
    GYROSCOPE_DB_ERROR = "GYROSCOPE_DB_ERROR"
    ACCELEROMETER_DB_ERROR = "ACCELEROMETER_DB_ERROR"
    RATIO_WAVE_DB_ERROR = "RATIO_WAVE_DB_ERROR"
    ATMOSPHERIC_PRESSURE_DB_ERROR = "ATMOSPHERIC_PRESSURE_DB_ERROR"
    GPS_DB_ERROR = "GPS_DB_ERROR"
    FILE_UPLOAD_ERROR = "FILE_UPLOAD_ERROR"
    FILE_DOWNLOAD_ERROR = "FILE_DOWNLOAD_ERROR"


class InfrastructureError(HTTPException):
    def __init__(
        self,
        error_type: InfrastructureErrorType,
        status_code: int,
        detail: str,
    ) -> None:
        self._type = error_type
        super().__init__(
            status_code,
            detail=detail,
        )

    @property
    def type(
        self,
    ) -> InfrastructureErrorType:
        return self._type
