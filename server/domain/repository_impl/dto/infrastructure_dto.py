from dataclasses import dataclass


@dataclass
class FloorRepositoryDto:
    floor_id: str
    floor_name: str
    building_id: str


@dataclass
class FloorInformationDto:
    floor_information_id: str
    floor_id: str


@dataclass
class FloorMapRepositoryDto:
    floor_map_id: str
    floor_information_id: str


@dataclass
class FpModelRepositoryDto:
    fp_model_id: str
    floor_information_id: str


@dataclass
class TrajectoryRepositoryDto:
    trajectory_id: str
    is_walking: bool
    pedestrian_id: str
    floor_information_id: str


@dataclass
class WalkingInformationRepositoryDto:
    walking_information_id: str
    pedestrian_id: str


@dataclass
class GyroscopeRepositoryDto:
    gyroscope_id: str
    walking_information_id: str


@dataclass
class AccelerometerRepositoryDto:
    accelerometer_id: str
    walking_information_id: str


@dataclass
class RatioWaveRepositoryDto:
    ratio_wave_id: str
    walking_information_id: str


@dataclass
class AtmosphericPressureRepositoryDto:
    atmospheric_pressure_id: str
    walking_information_id: str


@dataclass
class GpsRepositoryDto:
    gps_id: str
    walking_information_id: str


@dataclass
class WalkingSampleRepositoryDto:
    walking_sample_id: str
    is_converged: bool
    trajectory_id: str
    walking_information_id: str


@dataclass
class ParticleRepositoryDto:
    particle_id: str
    walking_sample_id: str
    particle_collection: bytes


@dataclass
class CoordinateRepositoryDto:
    coordinate_id: str
    x: float
    y: float
    floor_id: str


@dataclass
class WifiFingerprintingRepositoryDto:
    wifi_fingerprinting_id: str
    coordinate_id: str


@dataclass
class GeomagneticRepositoryDto:
    geomagnetic_id: str
    coordinate_id: str
