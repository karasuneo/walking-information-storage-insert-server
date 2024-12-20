from infrastructure.dto import FloorRepositoryDto
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection


class FloorRepository:
    def find_for_id(
        self,
        conn: connection,
        floor_id: str,
    ) -> FloorRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT level, name, building_id FROM floors WHERE id = %s",
                    (floor_id,),
                )

                result = cursor.fetchone()
                if result is not None:
                    level = result[0]
                    name = result[1]
                    building_id = result[2]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_FLOOR,
                        detail="Floor not found",
                        status_code=404,
                    )

                return FloorRepositoryDto(
                    id=floor_id,
                    name=name,
                    level=level,
                    building_id=building_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e
