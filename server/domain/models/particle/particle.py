import math
import secrets
from typing import Callable

from domain.dataclasses import Color, Coordinate


class Particle:
    def __init__(
        self,
        coordinate: Coordinate,
        weight: float,
        direction: float,
    ) -> None:
        self.__coordinate = coordinate
        self.__x = coordinate.x
        self.__y = coordinate.y
        self.__weight = weight
        self.__direction = direction

    @classmethod
    def create_random_particle(
        cls,
        x_range: int,
        y_range: int,
    ) -> "Particle":
        """## ランダムなパーティクルを生成する."""
        x = secrets.randbelow(x_range + 1)
        y = secrets.randbelow(y_range + 1)
        direction = secrets.randbelow(360)

        return Particle(
            coordinate=Coordinate(
                x=x,
                y=y,
            ),
            weight=1.0,
            direction=direction,
        )

    def get_coordinate(
        self,
    ) -> Coordinate:
        return self.__coordinate

    def get_direction(
        self,
    ) -> float:
        return self.__direction

    def get_color(
        self,
    ) -> Color:
        return self.__color

    def get_weight(
        self,
    ) -> float:
        return self.__weight

    def set_weight(
        self,
        weight: float,
    ) -> None:
        self.__weight = weight

    def set_color(
        self,
        color: Color,
    ) -> None:
        self.__color = color

    def new(
        self,
        weight: float,
        step: int,
        direction_error: float,
    ) -> "Particle":
        """## 指定されたパーティクルの座標と角度を元に新しいパーティクルを生成する."""
        if step < 0:
            new_x = int(self.__x + secrets.randbelow(abs(step) * 2 + 1) - step)
            new_y = int(self.__y + secrets.randbelow(abs(step) * 2 + 1) - step)
        else:
            new_x = int(self.__x + secrets.randbelow(step * 2 + 1) - step)
            new_y = int(self.__y + secrets.randbelow(step * 2 + 1) - step)
        new_direction = self.__direction + direction_error

        return Particle(
            coordinate=Coordinate(
                x=new_x,
                y=new_y,
            ),
            direction=new_direction,
            weight=weight,
        )

    def move(
        self,
        angle_change: float,
        step: int,
        step_error: int,
    ) -> "Particle":
        # 方向を変更
        move_direction = self.__direction + angle_change
        move_direction %= 360  # 0-359度に正規化

        # ステップとステップエラーを加算
        step_total = step + step_error

        # 角度をラジアンに変換
        radian = math.radians(move_direction)

        # 移動量を計算
        move_x = int(self.__x + step_total * math.cos(radian))
        move_y = int(self.__y + step_total * math.sin(radian))

        return Particle(
            coordinate=Coordinate(
                move_x,
                move_y,
            ),
            direction=move_direction,
            weight=self.__weight,
        )

    def is_straight_direction_to_wall(
        self,
        step: int,
        is_inside_floor: Callable[
            [Coordinate],
            bool,
        ],
    ) -> bool:
        """## パーティクルの歩幅以内に壁に向いているかを判定する."""
        radian = math.radians(self.__direction)

        for i in range(
            1,
            step + 1,
        ):
            move_x = int(self.__x + i * math.cos(radian))
            move_y = int(self.__y + i * math.sin(radian))

            if not is_inside_floor(
                Coordinate(
                    x=move_x,
                    y=move_y,
                ),
            ):
                return True

        return False

    def is_turn_direction_to_wall(
        self,
        step: int,
        is_inside_floor: Callable[
            [Coordinate],
            bool,
        ],
    ) -> bool:
        """## 90度回転したパーティクルが壁に埋まっているかを判定する."""
        plus_turn_move_particle = self.move(
            angle_change=90,
            step=step,
            step_error=0,
        )
        minus_turn_move_particle = self.move(
            step=step,
            angle_change=-90,
            step_error=0,
        )

        return not is_inside_floor(
            Coordinate(
                x=plus_turn_move_particle.get_coordinate().x,
                y=plus_turn_move_particle.get_coordinate().y,
            ),
        ) and not is_inside_floor(
            Coordinate(
                x=minus_turn_move_particle.get_coordinate().x,
                y=minus_turn_move_particle.get_coordinate().y,
            ),
        )

    def is_inside_circle(
        self,
        circle_center_position: Coordinate,
        radius: int,
    ) -> bool:
        """## 指定された座標が円の中にあるかどうかを判定する."""
        (
            cx,
            cy,
        ) = (
            circle_center_position.x,
            circle_center_position.y,
        )
        (
            px,
            py,
        ) = (
            self.__x,
            self.__y,
        )

        # 円の中心と点との距離を計算
        distance = math.sqrt((px - cx) * (px - cx) + (py - cy) * (py - cy))

        # 距離が半径以下であれば円の中にある
        return distance <= radius
