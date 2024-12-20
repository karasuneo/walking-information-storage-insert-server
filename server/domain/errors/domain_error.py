from enum import Enum

from fastapi import HTTPException


class DomainErrorType(Enum):
    INVALID_GYROSCOPE_DATA = "InvalidGyroscopeData"
    DEPICT_RECTANGLE_FAILED = "DepictRectangleFailed"
    COVERAGE_POSITION_IS_NONE = "CoveragePositionIsNone"
    REVERSED_ESTIMATION_PARTICLE_FILTER = "ReversedEstimationParticleFilter"


class DomainError(HTTPException):
    def __init__(
        self,
        error_type: DomainErrorType,
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
    ) -> DomainErrorType:
        return self._type
