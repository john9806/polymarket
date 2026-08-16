from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query

from recommender.pipeline import RecommendationPipeline


pipeline = RecommendationPipeline()


@asynccontextmanager
async def lifespan(_: FastAPI):
    pipeline.train_from_sources(
        path=os.getenv("BETS_DATA_PATH"),
        url=os.getenv("BETS_DATA_URL"),
    )
    yield


app = FastAPI(title="Polymarket Recommendation API", lifespan=lifespan)


@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: str, k: int = Query(5, ge=1, le=50)) -> dict[str, object]:
    recommendations = pipeline.recommend(user_id=user_id, k=k)
    return {"user_id": user_id, "recommendations": recommendations}
