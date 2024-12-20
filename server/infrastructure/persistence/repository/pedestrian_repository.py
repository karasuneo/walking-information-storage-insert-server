from domain.repository_impl.pedestrian_repository_impl import PedestrianRepositoryImpl
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection
from ulid import ULID


class PedestrianRepository(PedestrianRepositoryImpl):
    def save(
        self,
        conn: connection,
    ) -> None:
        with conn, conn.cursor() as cursor:
            try:
                pedestrian_id = str(ULID())
                cursor.execute(
                    "INSERT INTO pedestrians (id) VALUES (%s)",
                    (pedestrian_id,),
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.PEDESTRIAN_DB_ERROR,
                    500,
                    "Failed to save pedestrian",
                ) from e
