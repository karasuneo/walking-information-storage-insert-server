from abc import ABCMeta, abstractmethod

from domain.repository_impl.dto.infrastructure_dto import (
    FloorInformationDto,
    FloorMapRepositoryDto,
    FloorRepositoryDto,
    FpModelRepositoryDto,
)
from psycopg2.extensions import connection


class FloorRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        floor_name: str,
        building_id: str,
    ) -> FloorRepositoryDto:
        pass

    @abstractmethod
    def find_for_id(
        self,
        conn: connection,
        floor_id: str,
    ) -> FloorRepositoryDto:
        pass

    @abstractmethod
    def update(
        self,
        conn: connection,
        floor_id: str,
    ) -> None:
        pass


class FloorInformationRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        floor_id: str,
    ) -> FloorInformationDto:
        pass

    @abstractmethod
    def find_for_id(
        self,
        conn: connection,
        floor_information_id: str,
    ) -> FloorInformationDto:
        pass

    @abstractmethod
    def find_latest(
        self,
        conn: connection,
    ) -> FloorInformationDto:
        pass


class FloorMapRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        floor_information_id: str,
        floor_map: bytes,
    ) -> FloorMapRepositoryDto:
        pass

    @abstractmethod
    def find_for_floor_information_id(
        self,
        conn: connection,
        floor_information_id: str,
    ) -> FloorMapRepositoryDto:
        pass


class FpModelRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        fp_model_id: str,
        fp_model: bytes,
    ) -> FpModelRepositoryDto:
        pass
