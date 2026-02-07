from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = [
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
]


@dataclass(frozen=True)
class AnalyticsResult:
    total_count: int
    averages: dict[str, float | None]
    type_distribution: dict[str, int]

    def to_json(self) -> dict:
        return {
            "total_count": self.total_count,
            "averages": self.averages,
            "type_distribution": self.type_distribution,
        }


def compute_summary_analytics(df: pd.DataFrame) -> AnalyticsResult:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    total_count = int(len(df))

    flow = pd.to_numeric(df["Flowrate"], errors="coerce")
    pressure = pd.to_numeric(df["Pressure"], errors="coerce")
    temp = pd.to_numeric(df["Temperature"], errors="coerce")

    def _mean(series: pd.Series) -> float | None:
        value = series.dropna().mean()
        if pd.isna(value):
            return None
        return float(value)

    averages = {
        "Flowrate": _mean(flow),
        "Pressure": _mean(pressure),
        "Temperature": _mean(temp),
    }

    type_distribution = (
        df["Type"].fillna("Unknown").astype(str).value_counts(dropna=False).to_dict()
    )
    type_distribution = {str(k): int(v) for k, v in type_distribution.items()}

    return AnalyticsResult(
        total_count=total_count,
        averages=averages,
        type_distribution=type_distribution,
    )


def preview_rows(df: pd.DataFrame, limit: int) -> dict:
    limit = max(1, min(int(limit), 500))
    head = df.head(limit).copy()
    head = head.where(pd.notnull(head), None)
    return {
        "columns": [str(c) for c in head.columns.tolist()],
        "rows": head.to_dict(orient="records"),
        "limit": limit,
        "returned": int(len(head)),
    }
