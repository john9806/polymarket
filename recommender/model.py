from __future__ import annotations

import math
from collections import defaultdict

from .data import BetEvent


class PolymarketRecommender:
    def __init__(self) -> None:
        self.user_market_weights: dict[str, dict[str, float]] = {}
        self.market_popularity: dict[str, float] = {}

    def fit(self, events: list[BetEvent]) -> None:
        user_market_totals: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        market_totals: dict[str, float] = defaultdict(float)

        for event in events:
            user_id = event["user_id"]
            market_id = event["market_id"]
            amount = float(event["amount"])
            user_market_totals[user_id][market_id] += amount
            market_totals[market_id] += amount

        self.user_market_weights = {user: dict(markets) for user, markets in user_market_totals.items()}
        self.market_popularity = dict(market_totals)

    def _cosine_similarity(self, left: dict[str, float], right: dict[str, float]) -> float:
        if not left or not right:
            return 0.0
        common = set(left).intersection(right)
        if not common:
            return 0.0
        dot = sum(left[m] * right[m] for m in common)
        left_norm = math.sqrt(sum(v * v for v in left.values()))
        right_norm = math.sqrt(sum(v * v for v in right.values()))
        if left_norm == 0.0 or right_norm == 0.0:
            return 0.0
        return dot / (left_norm * right_norm)

    def recommend(self, user_id: str, k: int = 5) -> list[dict[str, float]]:
        k = max(1, k)
        seen_markets = set(self.user_market_weights.get(user_id, {}))
        target = self.user_market_weights.get(user_id)
        scored: dict[str, float] = defaultdict(float)

        if target:
            for other_user, other_markets in self.user_market_weights.items():
                if other_user == user_id:
                    continue
                similarity = self._cosine_similarity(target, other_markets)
                if similarity <= 0:
                    continue
                for market_id, amount in other_markets.items():
                    if market_id in seen_markets:
                        continue
                    scored[market_id] += similarity * amount

        if not scored:
            for market_id, popularity in self.market_popularity.items():
                if market_id not in seen_markets:
                    scored[market_id] = popularity

        ranked = sorted(scored.items(), key=lambda item: item[1], reverse=True)[:k]
        return [{"market_id": market_id, "score": score} for market_id, score in ranked]
