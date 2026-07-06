from travel_film_maker.core.asset import Asset
from travel_film_maker.edit.selector import build_timeline


def test_build_timeline_orders_assets_by_rating():
    low = Asset(id="low", type="photo", path="low.jpg", technical={"rating": 0.1})
    high = Asset(id="high", type="photo", path="high.jpg", technical={"rating": 0.9})

    timeline = build_timeline([low, high], fps=25)

    assert timeline.video_clips[0].asset_id == "high"
