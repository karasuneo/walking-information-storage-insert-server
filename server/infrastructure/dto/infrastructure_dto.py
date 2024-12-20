from dataclasses import dataclass


@dataclass
class BuildingRepositoryDto:
    id: str
    name: str
    latitude: float
    longitude: float


@dataclass
class FloorRepositoryDto:
    id: str
    name: str
    level: int
    building_id: str


@dataclass
class FloorInformationDto:
    id: str
    floor_id: str


@dataclass
class CoordinateRepositoryDto:
    id: int
    x: int
    y: int
    floor_id: str


@dataclass
class WifiFingerprintingRepositoryDto:
    id: str
    coordinate_id: int
