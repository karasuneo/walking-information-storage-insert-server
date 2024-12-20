from __future__ import annotations

from io import BytesIO

import pandas as pd


class RatioWaveFingerprint:
    def __init__(self, fp_model_file: bytes, ratio_wave_file: bytes) -> None:
        self.fp_model_df = pd.read_csv(BytesIO(fp_model_file))
        self.ratio_wave_df = pd.read_csv(BytesIO(ratio_wave_file))

    def aggregate_rssi_by_mac_address(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.groupby("mac_address", as_index=False).agg(
            {"gets": "first", "rssi": "mean", "type": "first"}
        )

        result["rssi"] = result["rssi"].round().astype(int)

        return result

    def calculate_match_rate(
        self, fp_model_df: pd.DataFrame, ratio_wave_df: pd.DataFrame
    ) -> float:
        fp_model_mac_addresses = set(fp_model_df["mac_address"])
        ratio_wave_mac_addresses = set(ratio_wave_df["mac_address"])

        intersection_count = len(
            fp_model_mac_addresses.intersection(ratio_wave_mac_addresses)
        )
        total_count = len(fp_model_mac_addresses.union(ratio_wave_mac_addresses))

        return (intersection_count / total_count) * 100 if total_count > 0 else 0
