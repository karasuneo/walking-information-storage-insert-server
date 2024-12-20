from config.const import CANDIDATE_PARTICLES_COLOR, PARTICLE_OUTLINE_COLOR
from domain.models.estimated_particle.estimated_particle import EstimatedParticle
from domain.models.floor_map.floor_map import FloorMap


class ParticleFloorMap:
    @staticmethod
    def generate_image(
        floor_map: FloorMap,
        estimated_particle: EstimatedParticle,
    ) -> None:
        floor_map_copy = floor_map.clone()

        # パーティクルの位置を描画
        for particle in estimated_particle:
            floor_map_copy.depict_circle(
                position=(
                    particle.get_coordinate().x,
                    particle.get_coordinate().y,
                ),
                color=CANDIDATE_PARTICLES_COLOR,
                outline_color=PARTICLE_OUTLINE_COLOR,
            )

        floor_map_copy.get_floor_map().copy().save("particle_floor_map.png")
