from __future__ import annotations

from math import sqrt
from typing import Iterable


def regression_metrics(observed: Iterable[float], predicted: Iterable[float]) -> dict[str, float]:
    obs = list(observed)
    pred = list(predicted)
    if len(obs) != len(pred) or not obs:
        raise ValueError("observed and predicted must have the same non-zero length")
    errors = [p - o for o, p in zip(obs, pred)]
    mae = sum(abs(e) for e in errors) / len(errors)
    rmse = sqrt(sum(e * e for e in errors) / len(errors))
    mape_terms = [abs(e / o) for o, e in zip(obs, errors) if o != 0]
    return {
        "n": len(obs),
        "mae": round(mae, 6),
        "rmse": round(rmse, 6),
        "mape": round(100 * sum(mape_terms) / len(mape_terms), 6) if mape_terms else 0.0,
    }
