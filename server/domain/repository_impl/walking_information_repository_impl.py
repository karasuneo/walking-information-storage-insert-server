from abc import ABCMeta, abstractmethod

from domain.repository_impl.dto.infrastructure_dto import (
    AccelerometerRepositoryDto,
    AtmosphericPressureRepositoryDto,
    GpsRepositoryDto,
    GyroscopeRepositoryDto,
    RatioWaveRepositoryDto,
    WalkingInformationRepositoryDto,
)
from psycopg2.extensions import connection


class WalkingInformationRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        pedestrian_id: str,
    ) -> WalkingInformationRepositoryDto:
        pass


class GyroscopeRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> GyroscopeRepositoryDto:
        pass


class AccelerometerRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> AccelerometerRepositoryDto:
        pass


class RatioWaveRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> RatioWaveRepositoryDto:
        pass


class AtmosphericPressureRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> AtmosphericPressureRepositoryDto:
        pass


class GpsRepositoryImpl(metaclass=ABCMeta):
    @abstractmethod
    def save(
        self,
        conn: connection,
        walking_information_id: str,
    ) -> GpsRepositoryDto:
        pass
