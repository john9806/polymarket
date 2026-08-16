from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests


BetEvent = dict[str, Any]


def _normalize_event(event: BetEvent) -> BetEvent | None:
    user_id = event.get("user_id")
    market_id = event.get("market_id")
    amount = event.get("amount", 1)
    if not user_id or not market_id:
        return None
    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        return None
    if amount_value <= 0:
        return None
    return {"user_id": str(user_id), "market_id": str(market_id), "amount": amount_value}


def _parse_events(raw: Any) -> list[BetEvent]:
    if not isinstance(raw, list):
        return []
    events: list[BetEvent] = []
    for item in raw:
        if isinstance(item, dict):
            normalized = _normalize_event(item)
            if normalized is not None:
                events.append(normalized)
    return events


def fetch_bets_from_file(path: str | Path) -> list[BetEvent]:
    with Path(path).open("r", encoding="utf-8") as file:
        raw = json.load(file)
    return _parse_events(raw)


def fetch_bets_from_url(url: str, timeout: float = 10.0) -> list[BetEvent]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError(f"Invalid JSON payload from {url}") from exc
    return _parse_events(payload)


def gather_bets(path: str | Path | None = None, url: str | None = None) -> list[BetEvent]:
    events: list[BetEvent] = []
    if path:
        events.extend(fetch_bets_from_file(path))
    if url:
        events.extend(fetch_bets_from_url(url))
    return events
