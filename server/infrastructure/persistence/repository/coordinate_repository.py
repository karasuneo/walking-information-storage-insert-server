from infrastructure.dto import CoordinateRepositoryDto
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection


class CoordinateRepository:
    def find_for_coordinate(
        self,
        conn: connection,
        x: int,
        y: int,
    ) -> CoordinateRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT id, floor_id FROM coordinates WHERE x = %s AND y = %s",
                    (x, y),
                )

                result = cursor.fetchone()
                if result is not None:
                    coordinate_id = result[0]
                    floor_id = result[1]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_COORDINATE,
                        detail="Floor not found",
                        status_code=404,
                    )

                return CoordinateRepositoryDto(
                    id=coordinate_id,
                    x=x,
                    y=y,
                    floor_id=floor_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.COORDINATE_DB_ERROR,
                    detail="Error occurred in coordinate database",
                    status_code=500,
                ) from e
