from application.dto import MovePedestrianServiceDto
from application.errors import ApplicationError, ApplicationErrorType
from config.const import STEP
from domain.models.estimated_particle.estimated_particle import EstimatedParticle
from domain.models.floor_map.floor_map import FloorMap
from domain.models.walking_parameter.walking_parameter import WalkingParameter
from domain.repository_impl import (
    AccelerometerRepositoryImpl,
    AtmosphericPressureRepositoryImpl,
    FloorInformationRepositoryImpl,
    FloorMapRepositoryImpl,
    FloorRepositoryImpl,
    GpsRepositoryImpl,
    GyroscopeRepositoryImpl,
    ParticleRepositoryImpl,
    PoseRepositoryImpl,
    RatioWaveRepositoryImpl,
    TrajectoryRepositoryImpl,
    WalkingInformationRepositoryImpl,
    WalkingSampleRepositoryImpl,
)
from infrastructure.connection import DBConnection, MinIOConnection
from infrastructure.errors.infrastructure_error import InfrastructureError, InfrastructureErrorType
from infrastructure.external.services import FileService
from utils import (
    get_accelerometer_bucket_name,
    get_atmospheric_pressure_bucket_name,
    get_floor_map_bucket_name,
    get_gps_bucket_name,
    get_gyroscope_bucket_name,
    get_ratio_wave_bucket_name,
)


class MovePedestrianService:
    def __init__(
        self,
        floor_repo: FloorRepositoryImpl,
        particle_repo: ParticleRepositoryImpl,
        floor_map_repo: FloorMapRepositoryImpl,
        gps_repo: GpsRepositoryImpl,
        gyroscope_repo: GyroscopeRepositoryImpl,
        ratio_wave_repo: RatioWaveRepositoryImpl,
        accelerometer_repo: AccelerometerRepositoryImpl,
        atmospheric_pressure_repo: AtmosphericPressureRepositoryImpl,
        trajectory_repo: TrajectoryRepositoryImpl,
        walking_sample_repo: WalkingSampleRepositoryImpl,
        floor_information_repo: FloorInformationRepositoryImpl,
        pose_repo: PoseRepositoryImpl,
        walking_information_repo: WalkingInformationRepositoryImpl,
    ) -> None:
        self.__floor_repo = floor_repo
        self.__particle_repo = particle_repo
        self.__floor_map_repo = floor_map_repo
        self.__gps_repo = gps_repo
        self.__gyroscope_repo = gyroscope_repo
        self.__ratio_wave_repo = ratio_wave_repo
        self.__accelerometer_repo = accelerometer_repo
        self.__atmospheric_pressure_repo = atmospheric_pressure_repo
        self.__trajectory_repo = trajectory_repo
        self.__walking_sample_repo = walking_sample_repo
        self.__floor_information_repo = floor_information_repo
        self.__pose_repo = pose_repo
        self.__walking_information_repo = walking_information_repo

    def run(
        self,
        pedestrian_id: str,
        trajectory_id: str,
        gps_file: bytes,
        wifi_file: bytes,
        gyroscope_file: bytes,
        accelerometer_file: bytes,
        atmospheric_pressure_file: bytes,
    ) -> MovePedestrianServiceDto:
        conn = DBConnection.connect()
        s3 = MinIOConnection.connect()
        file_service = FileService(s3)

        try:
            self.__trajectory_repo.find_for_id(
                conn=conn,
                trajectory_id=trajectory_id,
            )
        except InfrastructureError as e:
            if e.type == InfrastructureErrorType.NOT_FOUND_TRAJECTORY:
                raise ApplicationError(
                    error_type=ApplicationErrorType.NOT_WALKING_START,
                    status_code=404,
                    detail="Trajectory not found.",
                ) from e

        # 歩行データから、歩行パラメータを取得
        walking_parameter = WalkingParameter(
            step=STEP,
            gyroscope_file=gyroscope_file,
        )

        # 歩行情報
        walking_information_infrastructure_dto = self.__walking_information_repo.save(
            conn=conn,
            pedestrian_id=pedestrian_id,
        )
        walking_information_id = (
            walking_information_infrastructure_dto.walking_information_id
        )

        # 引数のidを元に、必要な情報を取得
        trajectory_infrastructure_dto = self.__trajectory_repo.find_for_id(
            conn=conn,
            trajectory_id=trajectory_id,
        )
        floor_information_id = trajectory_infrastructure_dto.floor_information_id

        floor_map_infrastructure_dto = (
            self.__floor_map_repo.find_for_floor_information_id(
                conn=conn,
                floor_information_id=floor_information_id,
            )
        )
        floor_map_id = floor_map_infrastructure_dto.floor_map_id

        floor_information_infrastructure_dto = (
            self.__floor_information_repo.find_for_id(
                conn=conn,
                floor_information_id=floor_information_id,
            )
        )
        floor_id = floor_information_infrastructure_dto.floor_id

        floor_map_image_bytes = file_service.download(
            key=get_floor_map_bucket_name(
                floor_id=floor_id,
                floor_information_id=floor_information_id,
                floor_map_id=floor_map_id,
            ),
        )
        floor_map = FloorMap(
            floor_map_image_bytes=floor_map_image_bytes,
        )

        try:
            walking_sample_infrastructure_dto = (
                self.__walking_sample_repo.find_latest_for_trajectory_id(
                    conn=conn,
                    trajectory_id=trajectory_id,
                )
            )
        except InfrastructureError as e:
            if e.type == InfrastructureErrorType.NOT_FOUND_WALKING_SAMPLE:
                estimated_particle = EstimatedParticle.initialize(
                    floor_map=floor_map,
                    initial_walking_parameter=walking_parameter,
                )
            else:
                raise ApplicationError(
                    error_type=ApplicationErrorType.UNKNOWN,
                    status_code=500,
                    detail="An unknown error occurred.",
                ) from e
        else:
            walking_sample_id = walking_sample_infrastructure_dto.walking_sample_id
            # 最新のパーティクルの状態を取得
            latest_particle_collection = (
                self.__particle_repo.find_for_walking_sample_id(
                    conn=conn,
                    walking_sample_id=walking_sample_id,
                )
            )
            estimated_particle = EstimatedParticle(
                floor_map=floor_map,
                current_walking_parameter=walking_parameter,
                particle_collection=latest_particle_collection,
            )

        # パーティクルフィルタの実行
        estimated_particle.remove_by_floor_map()
        move_estimation_particles = estimated_particle.move(
            current_walking_parameter=walking_parameter,
        )
        move_estimation_particles.remove_by_floor_map()
        move_estimation_particles.remove_by_direction(step=walking_parameter.get_step())
        move_estimation_particles.resampling(step=walking_parameter.get_step())

        # その時点で、パーティクルフィルタをかけた時の推定位置を取得
        estimated_pose = move_estimation_particles.get_estimated_pose()

        # パーティクルフィルタの結果を保存
        walking_sample = self.__walking_sample_repo.save(
            conn=conn,
            is_converged=move_estimation_particles.is_converged(),
            trajectory_id=trajectory_id,
            walking_information_id=walking_information_id,
        )
        walking_sample_id = walking_sample.walking_sample_id

        _ = self.__particle_repo.save_all(
            conn=conn,
            walking_sample_id=walking_sample_id,
            particle_collection=move_estimation_particles.get_particle_collection(),
        )

        # 推定位置を保存
        self.__pose_repo.save(
            conn=conn,
            estimated_pose=estimated_pose,
            walking_sample_id=walking_sample_id,
        )

        # 歩行情報を保存
        walking_information_infrastructure_dto = self.__walking_information_repo.save(
            conn=conn,
            pedestrian_id=pedestrian_id,
        )
        walking_information_id = (
            walking_information_infrastructure_dto.walking_information_id
        )

        gps = self.__gps_repo.save(
            conn=conn,
            walking_information_id=walking_information_id,
        )
        file_service.upload(
            key=get_gps_bucket_name(
                pedestrian_id=pedestrian_id,
                walking_information_id=walking_information_id,
                gps_id=gps.gps_id,
            ),
            file=gps_file,
        )

        ratio_wave = self.__ratio_wave_repo.save(
            conn=conn,
            walking_information_id=walking_information_id,
        )
        file_service.upload(
            key=get_ratio_wave_bucket_name(
                pedestrian_id=pedestrian_id,
                walking_information_id=walking_information_id,
                ratio_wave_id=ratio_wave.ratio_wave_id,
            ),
            file=wifi_file,
        )

        gyroscope = self.__gyroscope_repo.save(
            conn=conn,
            walking_information_id=walking_information_id,
        )
        file_service.upload(
            key=get_gyroscope_bucket_name(
                pedestrian_id=pedestrian_id,
                walking_information_id=walking_information_id,
                gyroscope_id=gyroscope.gyroscope_id,
            ),
            file=gyroscope_file,
        )

        accelerometer = self.__accelerometer_repo.save(
            conn=conn,
            walking_information_id=walking_information_id,
        )
        file_service.upload(
            key=get_accelerometer_bucket_name(
                pedestrian_id=pedestrian_id,
                walking_information_id=walking_information_id,
                accelerometer_id=accelerometer.accelerometer_id,
            ),
            file=accelerometer_file,
        )

        atmospheric_pressure = self.__atmospheric_pressure_repo.save(
            conn=conn,
            walking_information_id=walking_information_id,
        )
        file_service.upload(
            key=get_atmospheric_pressure_bucket_name(
                pedestrian_id=pedestrian_id,
                walking_information_id=walking_information_id,
                atmospheric_pressure_id=atmospheric_pressure.atmospheric_pressure_id,
            ),
            file=atmospheric_pressure_file,
        )

        return MovePedestrianServiceDto(
            pose=estimated_pose,
            walking_parameter=walking_parameter,
        )
