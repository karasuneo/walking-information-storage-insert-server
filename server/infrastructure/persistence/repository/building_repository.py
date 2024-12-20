from infrastructure.dto import BuildingRepositoryDto
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection


class BuildingRepository:
    def find_for_id(
        self,
        conn: connection,
        building_id: str,
    ) -> BuildingRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT name, latitude, longitude FROM buildings WHERE id = %s",
                    (building_id,),
                )

                result = cursor.fetchone()
                if result is not None:
                    name = result[0]
                    latitude = result[1]
                    longitude = result[2]
                else:
                    raise InfrastructureError(
                        InfrastructureErrorType.NOT_FOUND_BUILDING,
                        detail="Floor not found",
                        status_code=404,
                    )

                return BuildingRepositoryDto(
                    id=building_id,
                    name=name,
                    latitude=latitude,
                    longitude=longitude,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.FLOOR_DB_ERROR,
                    detail="Error occurred in floor database",
                    status_code=500,
                ) from e
