from __future__ import annotations

from travel_film_maker.core.asset import Asset


def score_assets(assets: list[Asset]) -> list[Asset]:
    for asset in assets:
        asset.technical.setdefault("rating", _baseline_rating(asset))
    return assets


def _baseline_rating(asset: Asset) -> float:
    if asset.type == "video":
        return 0.75
    return 0.7
