from dataclasses import dataclass

from domain.dataclasses import Pose
from domain.models.walking_parameter.walking_parameter import WalkingParameter


@dataclass
class StartWalkingServiceDto:
    trajectory_id: str
    floor_information_id: str


@dataclass
class MovePedestrianServiceDto:
    pose: Pose
    walking_parameter: WalkingParameter


@dataclass
class FinishWalkingServiceDto:
    trajectory_id: str
