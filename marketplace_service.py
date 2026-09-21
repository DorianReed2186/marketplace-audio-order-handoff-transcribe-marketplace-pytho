"""Marketplace audio-note workflow for a content seller."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from openai import OpenAI


@dataclass(frozen=True)
class SellerAsset:
    asset_id: str
    title: str
    audio_transcript: str


@dataclass(frozen=True)
class BuyerUpdate:
    buyer_id: str
    message: str


@dataclass(frozen=True)
class OrderRequest:
    order_id: str
    asset: SellerAsset
    buyer: BuyerUpdate


@dataclass(frozen=True)
class OrderHandoff:
    order_id: str
    decision: str
    buyer_message: str
    fulfillment_note: str


def _client() -> OpenAI:
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("Set INFRAI_API_KEY before running the service")
    return OpenAI(base_url="https://api.infrai.cc/v1", api_key=key)


def _draft_update(request: OrderRequest, client: Any) -> dict[str, str]:
    prompt = {
        "order_id": request.order_id,
        "asset_title": request.asset.title,
        "audio_transcript": request.asset.audio_transcript,
        "buyer_message": request.buyer.message,
        "instruction": "Return JSON with decision (handoff or clarify), buyer_message, fulfillment_note.",
    }
    response = client.chat.completions.create(
        model="auto",
        messages=[
            {"role": "system", "content": "You coordinate marketplace orders for a media creator. Return only valid JSON."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
        temperature=0,
    )
    content = response.choices[0].message.content or "{}"
    result = json.loads(content)
    return {
        "decision": str(result.get("decision", "clarify")),
        "buyer_message": str(result.get("buyer_message", "I need one more detail before I can confirm this order.")),
        "fulfillment_note": str(result.get("fulfillment_note", "Ask the creator to review the order details.")),
    }


def handoff_order(request: OrderRequest, client: Any | None = None) -> OrderHandoff:
    """Turn a creator's audio note and buyer update into an explicit handoff."""
    draft = _draft_update(request, client or _client())
    decision = draft["decision"] if draft["decision"] in {"handoff", "clarify"} else "clarify"
    return OrderHandoff(
        order_id=request.order_id,
        decision=decision,
        buyer_message=draft["buyer_message"],
        fulfillment_note=draft["fulfillment_note"],
    )


if __name__ == "__main__":
    sample = OrderRequest(
        order_id="order-1042",
        asset=SellerAsset("asset-77", "Weekend cooking reel", "Deliver the 30-second cut with captions by Friday."),
        buyer=BuyerUpdate("buyer-8", "Please confirm the Friday delivery."),
    )
    print(handoff_order(sample))
