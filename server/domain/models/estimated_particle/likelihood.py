from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from domain.models.particle.particle import Particle
    from numpy.typing import NDArray

import io

import pandas as pd


class Likelihood:
    def __init__(self, model: bytes) -> None:
        self.__rssi_model_df = pd.read_csv(io.BytesIO(model))
        self.__x = np.linspace(
            0, int(max(self.__rssi_model_df["x"])), int(max(self.__rssi_model_df["x"]))
        )
        self.__y = np.linspace(
            0, int(max(self.__rssi_model_df["y"])), int(max(self.__rssi_model_df["y"]))
        )
        self.__X, self.__Y = np.meshgrid(self.__x, self.__y)
        self.__rssi = self.__rssi_model_df["rssi"].to_numpy().reshape(self.__X.shape)
        self.__std_dev = np.std(self.__rssi)

        # キャッシュを初期化
        self.__likelihood_cache: dict[float, NDArray[np.float64]] = {}

    def __generate_likelihood_function(self, rssi_input: float) -> NDArray[np.float64]:
        """## rssiを受け取り、rssiモデルを元に座標の確率密度関数を作成する"""
        # キャッシュをチェック
        if rssi_input in self.__likelihood_cache:
            return self.__likelihood_cache[rssi_input]

        # RSSI値と入力されたRSSI値との差を計算
        rssi_difference = self.__rssi - rssi_input

        # 尤度関数を計算
        likelihood = np.exp(-0.5 * (rssi_difference / self.__std_dev) ** 2) / (
            self.__std_dev * np.sqrt(2 * np.pi)
        )

        # 尤度を正規化して総和が1になるようにする
        likelihood /= np.sum(likelihood)

        # キャッシュに保存
        self.__likelihood_cache[rssi_input] = likelihood

        return likelihood

    def __get_likelihood_from_coordinate(
        self, coordinate: tuple[int, int], likelihood: NDArray[np.float64]
    ) -> float:
        """## 座標を入力して尤度を取得"""
        x, y = coordinate
        # 座標の範囲チェック
        if (
            x < self.__X.min()
            or x > self.__X.max()
            or y < self.__Y.min()
            or y > self.__Y.max()
        ):
            return 0.0

        # 座標に最も近いインデックスを取得
        idx_x = (np.abs(self.__X[0, :] - x)).argmin()
        idx_y = (np.abs(self.__Y[:, 0] - y)).argmin()

        return float(likelihood[idx_y, idx_x])

    def get_likelihood(self, particle: Particle, rssi: float) -> float:
        """## パーティクルの尤度を取得する."""
        likelihood = self.__generate_likelihood_function(rssi)
        return self.__get_likelihood_from_coordinate(
            (particle.get_coordinate().x, particle.get_coordinate().y), likelihood
        )
