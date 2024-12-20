from domain.repository_impl import (
    AccelerometerRepositoryImpl,
    AtmosphericPressureRepositoryImpl,
    GpsRepositoryImpl,
    GyroscopeRepositoryImpl,
    RatioWaveRepositoryImpl,
    WalkingInformationRepositoryImpl,
)
from domain.repository_impl.dto.infrastructure_dto import (
    AccelerometerRepositoryDto,
    AtmosphericPressureRepositoryDto,
    GpsRepositoryDto,
    GyroscopeRepositoryDto,
    RatioWaveRepositoryDto,
    WalkingInformationRepositoryDto,
)
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from psycopg2.extensions import connection
from ulid import ULID


class WalkingInformationRepository(WalkingInformationRepositoryImpl):
    def save(
        self,
        conn: connection,
        pedestrian_id: str,
    ) -> WalkingInformationRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                walking_information_id = str(ULID())

                cursor.execute(
                    (
                        "INSERT INTO walking_information (id, pedestrian_id) "
                        "VALUES (%s, %s)"
                    ),
                    (
                        (walking_information_id),
                        pedestrian_id,
                    ),
                )

                return WalkingInformationRepositoryDto(
                    walking_information_id=walking_information_id,
                    pedestrian_id=pedestrian_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.WALKING_INFORMATION_DB_ERROR,
                    500,
                    "Failed to save walking information",
                ) from e


class GyroscopeRepository(GyroscopeRepositoryImpl):
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> GyroscopeRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                gyroscope_id = str(ULID())

                cursor.execute(
                    (
                        "INSERT INTO gyroscopes (id, walking_information_id) "
                        "VALUES (%s, %s)"
                    ),
                    (
                        (gyroscope_id),
                        walking_information_id,
                    ),
                )

                return GyroscopeRepositoryDto(
                    gyroscope_id=gyroscope_id,
                    walking_information_id=walking_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.GYROSCOPE_DB_ERROR,
                    500,
                    "Failed to save gyroscope",
                ) from e


class AccelerometerRepository(AccelerometerRepositoryImpl):
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> AccelerometerRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                accelerometer_id = str(ULID())

                cursor.execute(
                    (
                        "INSERT INTO accelerometers (id, walking_information_id) "
                        "VALUES (%s, %s)"
                    ),
                    (
                        (accelerometer_id),
                        walking_information_id,
                    ),
                )

                return AccelerometerRepositoryDto(
                    accelerometer_id=accelerometer_id,
                    walking_information_id=walking_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.ACCELEROMETER_DB_ERROR,
                    500,
                    "Failed to save accelerometer",
                ) from e


class RatioWaveRepository(RatioWaveRepositoryImpl):
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> RatioWaveRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                ratio_wave_id = str(ULID())

                cursor.execute(
                    "INSERT INTO ratio_waves (id, walking_information_id) "
                    "VALUES (%s, %s)",
                    (
                        (ratio_wave_id),
                        walking_information_id,
                    ),
                )

                return RatioWaveRepositoryDto(
                    ratio_wave_id=ratio_wave_id,
                    walking_information_id=walking_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.RATIO_WAVE_DB_ERROR,
                    500,
                    "Failed to save ratio wave",
                ) from e


class AtmosphericPressureRepository(AtmosphericPressureRepositoryImpl):
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> AtmosphericPressureRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                atmospheric_pressure_id = str(ULID())

                cursor.execute(
                    "INSERT INTO atmospheric_pressures (id, walking_information_id) "
                    "VALUES (%s, %s)",
                    (
                        (atmospheric_pressure_id),
                        walking_information_id,
                    ),
                )

                return AtmosphericPressureRepositoryDto(
                    atmospheric_pressure_id=atmospheric_pressure_id,
                    walking_information_id=walking_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.ATMOSPHERIC_PRESSURE_DB_ERROR,
                    500,
                    "Failed to save atmospheric pressure",
                ) from e


class GpsRepository(GpsRepositoryImpl):
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> GpsRepositoryDto:
        with conn, conn.cursor() as cursor:
            try:
                gps_id = str(ULID())

                cursor.execute(
                    "INSERT INTO gps (id, walking_information_id) VALUES (%s, %s)",
                    (
                        (gps_id),
                        walking_information_id,
                    ),
                )

                return GpsRepositoryDto(
                    gps_id=gps_id,
                    walking_information_id=walking_information_id,
                )

            except Exception as e:
                raise InfrastructureError(
                    InfrastructureErrorType.GPS_DB_ERROR,
                    500,
                    "Failed to save gps",
                ) from e
