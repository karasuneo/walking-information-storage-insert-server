from infrastructure.dto import WifiFingerprintingRepositoryDto
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection
from ulid import ULID


class WifiFingerPrintingRepository:
    def save(
        self,
        conn: connection,
        coordinate_id: int,
    ) -> WifiFingerprintingRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                wifi_printing_id = str(ULID())
                cursor.execute(
                    "INSERT INTO wifi_fingerprinting (id, coordinate_id) VALUES (%s, %s)",
                    (wifi_printing_id, coordinate_id),
                )

                return WifiFingerprintingRepositoryDto(
                    id=wifi_printing_id,
                    coordinate_id=coordinate_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.WIFI_FINGERPRINT_DB_ERROR,
                    detail="Error occurred in wifi fingerprint database",
                    status_code=500,
                ) from e
