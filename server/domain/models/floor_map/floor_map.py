from __future__ import annotations

import math
from io import BytesIO
from typing import TYPE_CHECKING

from config.const import INSIDE_PARTICLE_COLOR
from domain.dataclasses import Coordinate
from domain.errors.domain_error import DomainError, DomainErrorType
from PIL import Image, ImageDraw

if TYPE_CHECKING:
    from domain.dataclasses import Color
    from PIL.Image import Image as ImageType


class FloorMap:
    def __init__(
        self,
        floor_map_image_bytes: bytes,
    ) -> None:
        image_stream = BytesIO(floor_map_image_bytes)
        floor_map_image = Image.open(image_stream)

        self.__floor_map = floor_map_image
        self.__draw = ImageDraw.Draw(self.__floor_map)
        (
            self.__map_width,
            self.__map_height,
        ) = self.__floor_map.size

    def clone(self) -> FloorMap:
        return FloorMap(
            floor_map_image_bytes=self.__floor_map.tobytes(),
        )

    def get_floor_map(
        self,
    ) -> ImageType:
        return self.__floor_map

    def get_map_width(
        self,
    ) -> int:
        return self.__map_width

    def get_map_height(
        self,
    ) -> int:
        return self.__map_height

    def depict(
        self,
        position: tuple[
            int,
            int,
        ],
        color: Color,
    ) -> None:
        """## 指定した座標位置を描画する."""
        try:
            (
                x,
                y,
            ) = position
            self.__floor_map.putpixel(
                (
                    x,
                    y,
                ),
                [color.a, color.b, color.g, color.r],
            )
        except Exception as e:
            raise DomainError(
                error_type=DomainErrorType.DEPICT_RECTANGLE_FAILED,
                status_code=500,
                detail="Failed to depict the position.",
            ) from e

    def is_inside_floor(
        self,
        coordinate: Coordinate,
    ) -> bool:
        """## 指定した座標が歩行可能領域内に存在するかどうかを判定する."""
        (
            x,
            y,
        ) = (
            coordinate.x,
            coordinate.y,
        )

        if (
            0 <= x < self.__map_width
            and 0 <= y < self.__map_height
            and self.__floor_map.getpixel((x, y)) == INSIDE_PARTICLE_COLOR
        ):
            return True

        return False

    def get_nearest_inside_coordinate(
        self,
        outside_position: Coordinate,
        search_range: int,
    ) -> Coordinate:
        """## 指定した座標から最も近い歩行可能領域内の座標を取得する."""
        # すでに歩行可能領域内に存在する場合は引数をそのまま返す
        (
            x,
            y,
        ) = (
            outside_position.x,
            outside_position.y,
        )
        if self.is_inside_floor(outside_position):
            return outside_position

        for radius in range(
            1,
            search_range,
        ):
            for angle in range(
                0,
                360,
                10,
            ):
                estimated_x = int(x + radius * math.cos(math.radians(angle)))
                estimated_y = int(y + radius * math.sin(math.radians(angle)))

                if self.is_inside_floor(
                    Coordinate(
                        x=estimated_x,
                        y=estimated_y,
                    ),
                ):
                    return Coordinate(
                        x=estimated_x,
                        y=estimated_y,
                    )

        return outside_position
