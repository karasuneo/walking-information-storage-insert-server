from enum import Enum

from fastapi import HTTPException


class ApplicationErrorType(Enum):
    NOT_WALKING_START = "NotWalkingStart"
    NOT_FLOOR_INFORMATION = "NotFloorInformation"
    NOT_FLOOR_MAP = "NotFloorMap"
    NOT_FLOOR = "NotFloor"
    UNKNOWN = "Unknown"


class ApplicationError(HTTPException):
    def __init__(
        self,
        error_type: ApplicationErrorType,
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
    ) -> ApplicationErrorType:
        return self._type
