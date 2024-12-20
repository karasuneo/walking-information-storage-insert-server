from application.dto import StartWalkingServiceDto
from domain.repository_impl import FloorInformationRepositoryImpl, TrajectoryRepositoryImpl
from infrastructure.connection import DBConnection


class StartWalkingService:
    def __init__(
        self,
        trajectory_repo: TrajectoryRepositoryImpl,
        floor_information_repo: FloorInformationRepositoryImpl,
    ) -> None:
        self.__trajectory_repo = trajectory_repo
        self.__floor_information_repo = floor_information_repo

    def run(
        self,
        pedestrian_id: str,
    ) -> StartWalkingServiceDto:
        conn = DBConnection.connect()

        floor_information_infrastructure_dto = (
            self.__floor_information_repo.find_latest(conn=conn)
        )
        floor_information_id = floor_information_infrastructure_dto.floor_information_id

        trajectory_infrastructure_dto = self.__trajectory_repo.save(
            conn=conn,
            is_walking=True,
            pedestrian_id=pedestrian_id,
            floor_information_id=floor_information_id,
        )
        trajectory_id = trajectory_infrastructure_dto.trajectory_id

        return StartWalkingServiceDto(
            trajectory_id=trajectory_id,
            floor_information_id=floor_information_id,
        )
