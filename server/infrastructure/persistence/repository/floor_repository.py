from domain.repository_impl import (
    FloorInformationRepositoryImpl,
    FloorMapRepositoryImpl,
    FloorRepositoryImpl,
)
from domain.repository_impl.dto.infrastructure_dto import (
    FloorInformationDto,
    FloorMapRepositoryDto,
    FloorRepositoryDto,
)
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection
from ulid import ULID


class FloorRepository(FloorRepositoryImpl):
    def save(
        self,
        conn: connection,
        floor_name: str,
        building_id: str,
    ) -> FloorRepositoryDto:
        with conn:
            try:
                with conn.cursor() as cursor:
                    ulid = ULID()
                    cursor.execute(
                        "INSERT INTO floors (id, floor_name, building_id) "
                        "VALUES (%s, %s, %s) RETURNING id",
                        (
                            str(ulid),
                            floor_name,
                            building_id,
                        ),
                    )

                    result = cursor.fetchone()
                    if result is not None:
                        floor_id = result[0]
                    else:
                        raise InfrastructureError(
                            InfrastructureErrorType.NOT_FOUND_FLOOR,
                            detail="Floor not found",
                            status_code=404,
                        )

                    return FloorRepositoryDto(
                        floor_id=floor_id,
                        floor_name=floor_name,
                        building_id=building_id,
                    )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e

    def find_for_id(
        self,
        conn: connection,
        floor_id: str,
    ) -> FloorRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT floor_name, building_id FROM floors WHERE id = %s",
                    (floor_id,),
                )

                result = cursor.fetchone()
                if result is not None:
                    floor_name = result[0]
                    building_id = result[1]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_FLOOR,
                        detail="Floor not found",
                        status_code=404,
                    )

                return FloorRepositoryDto(
                    floor_id=floor_id,
                    floor_name=floor_name,
                    building_id=building_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e

    def update(
        self,
        conn: connection,
        floor_id: str,
    ) -> None:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "UPDATE floors SET floor_name = %s WHERE id = %s",
                    (floor_id),
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e


class FloorInformationRepository(FloorInformationRepositoryImpl):
    def save(
        self,
        conn: connection,
        floor_id: str,
    ) -> FloorInformationDto:
        with conn, conn.cursor() as cursor:
            try:
                floor_information_id = str(ULID())
                cursor.execute(
                    "INSERT INTO floor_information (id, floor_id) "
                    "VALUES (%s, %s) RETURNING id",
                    (
                        floor_information_id,
                        floor_id,
                    ),
                )

                result = cursor.fetchone()
                if result is not None:
                    floor_information_id = result[0]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_FLOOR_INFORMATION,
                        detail="Floor information not found",
                        status_code=404,
                    )

                return FloorInformationDto(
                    floor_information_id=floor_information_id,
                    floor_id=floor_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e

    def find_for_id(
        self,
        conn: connection,
        floor_information_id: str,
    ) -> FloorInformationDto:
        with conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT floor_id FROM floor_information WHERE id = %s",
                (floor_information_id,),
            )

            result = cursor.fetchone()
            if result is not None:
                floor_id = result[0]
            else:
                raise InfrastructureError(
                    InfrastructureErrorType.NOT_FOUND_FLOOR_INFORMATION,
                    detail="Floor information not found",
                    status_code=404,
                )

            return FloorInformationDto(
                floor_information_id=floor_information_id,
                floor_id=floor_id,
            )

    def find_latest(
        self,
        conn: connection,
    ) -> FloorInformationDto:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT id, floor_id FROM floor_information "
                    "ORDER BY created_at DESC LIMIT 1",
                )

                result = cursor.fetchone()
                if result is not None:
                    floor_information_id = result[0]
                    floor_id = result[1]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_FLOOR_INFORMATION,
                        detail="Floor information not found",
                        status_code=404,
                    )

                return FloorInformationDto(
                    floor_information_id=floor_information_id,
                    floor_id=floor_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_INFORMATION_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e


class FloorMapRepository(FloorMapRepositoryImpl):
    def save(
        self,
        conn: connection,
        floor_information_id: str,
        floor_map: bytes,
    ) -> FloorMapRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                floor_map_id = ULID()
                cursor.execute(
                    "INSERT INTO floor_maps (id, floor_information_id, floor_map) "
                    "VALUES (%s, %s, %s) RETURNING id",
                    (
                        floor_map_id,
                        floor_information_id,
                        floor_map,
                    ),
                )

                result = cursor.fetchone()
                if result is not None:
                    floor_map_id = result[0]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_FLOOR_MAP,
                        detail="Floor map not found",
                        status_code=404,
                    )

                return FloorMapRepositoryDto(
                    floor_map_id=floor_map_id,
                    floor_information_id=floor_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_MAP_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e

    def find_for_floor_information_id(
        self,
        conn: connection,
        floor_information_id: str,
    ) -> FloorMapRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT id FROM floor_maps WHERE floor_information_id = %s",
                    (floor_information_id,),
                )

                result = cursor.fetchone()
                if result is not None:
                    floor_id = result[0]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_FLOOR_MAP,
                        detail="Floor map not found",
                        status_code=404,
                    )

                return FloorMapRepositoryDto(
                    floor_map_id=floor_id,
                    floor_information_id=floor_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_MAP_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e
