from dataclasses import dataclass


@dataclass
class InsertFpModelDto:
    building_id: str
    floor_id: str
    x: int
    y: int
    fp_model_file: bytes
