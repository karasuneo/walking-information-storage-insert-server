from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class Pose:
    coordinate: Coordinate
    direction: float
