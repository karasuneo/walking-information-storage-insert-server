from abc import ABCMeta, abstractmethod

from domain.repository_impl.dto.infrastructure_dto import (
    CoordinateRepositoryDto,
    GeomagneticRepositoryDto,
    WifiFingerprintingRepositoryDto,
)
from psycopg2.extensions import connection


class CoordinateRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        floor_name: str,
        building_id: str,
    ) -> CoordinateRepositoryDto:
        pass

    @abstractmethod
    def find_for_id(
        self,
        conn: connection,
        floor_id: str,
    ) -> CoordinateRepositoryDto:
        pass


class GeomagneticRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        floor_id: str,
        geomagnetic_id: str,
    ) -> GeomagneticRepositoryDto:
        pass

    @abstractmethod
    def find_for_id(
        self,
        conn: connection,
        geomagnetic_id: str,
    ) -> GeomagneticRepositoryDto:
        pass


class WifiFingerprintingRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        coordinate_id: str,
        wifi_fingerprinting_id: str,
    ) -> WifiFingerprintingRepositoryDto:
        pass

    @abstractmethod
    def find_for_id(
        self,
        conn: connection,
        wifi_fingerprinting_id: str,
    ) -> WifiFingerprintingRepositoryDto:
        pass
