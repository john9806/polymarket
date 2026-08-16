from __future__ import annotations

from pathlib import Path

from .data import BetEvent, gather_bets
from .model import PolymarketRecommender

SAMPLE_EVENTS: list[BetEvent] = [
    {"user_id": "u1", "market_id": "m1", "amount": 10.0},
    {"user_id": "u1", "market_id": "m2", "amount": 6.0},
    {"user_id": "u2", "market_id": "m1", "amount": 8.0},
    {"user_id": "u2", "market_id": "m3", "amount": 12.0},
    {"user_id": "u3", "market_id": "m2", "amount": 9.0},
    {"user_id": "u3", "market_id": "m4", "amount": 11.0},
]


class RecommendationPipeline:
    def __init__(self) -> None:
        self.model = PolymarketRecommender()
        self.trained = False

    def train(self, events: list[BetEvent]) -> None:
        self.model.fit(events)
        self.trained = True

    def train_from_sources(self, path: str | Path | None = None, url: str | None = None) -> None:
        events = gather_bets(path=path, url=url)
        if not events:
            events = SAMPLE_EVENTS
        self.train(events)

    def recommend(self, user_id: str, k: int = 5) -> list[dict[str, float]]:
        if not self.trained:
            self.train(SAMPLE_EVENTS)
        return self.model.recommend(user_id=user_id, k=k)
