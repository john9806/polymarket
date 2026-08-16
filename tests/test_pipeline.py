from recommender.pipeline import RecommendationPipeline


def test_pipeline_recommends_from_similar_users() -> None:
    events = [
        {"user_id": "u1", "market_id": "m1", "amount": 10},
        {"user_id": "u1", "market_id": "m2", "amount": 5},
        {"user_id": "u2", "market_id": "m1", "amount": 8},
        {"user_id": "u2", "market_id": "m3", "amount": 20},
    ]

    pipeline = RecommendationPipeline()
    pipeline.train(events)

    recommendations = pipeline.recommend("u1", k=1)
    assert [item["market_id"] for item in recommendations] == ["m3"]
    assert recommendations[0]["score"] > 0


def test_pipeline_fallback_for_new_user_uses_popularity() -> None:
    events = [
        {"user_id": "u1", "market_id": "m1", "amount": 10},
        {"user_id": "u2", "market_id": "m2", "amount": 20},
        {"user_id": "u3", "market_id": "m2", "amount": 5},
    ]

    pipeline = RecommendationPipeline()
    pipeline.train(events)

    recommendations = pipeline.recommend("new-user", k=2)
    assert [item["market_id"] for item in recommendations] == ["m2", "m1"]
