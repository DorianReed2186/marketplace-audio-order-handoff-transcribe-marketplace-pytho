import json

from marketplace_service import BuyerUpdate, OrderRequest, SellerAsset, handoff_order


class Message:
    content = json.dumps({
        "decision": "handoff",
        "buyer_message": "Friday delivery is confirmed.",
        "fulfillment_note": "Prepare the captioned 30-second cut for Friday.",
    })


class Completions:
    def create(self, **kwargs):
        assert kwargs["model"] == "auto"
        assert "audio_transcript" in kwargs["messages"][1]["content"]
        return type("Response", (), {"choices": [type("Choice", (), {"message": Message()})()]})()


class FakeClient:
    chat = type("Chat", (), {"completions": Completions()})()


def test_creator_note_can_move_order_to_handoff():
    request = OrderRequest(
        "order-1042",
        SellerAsset("asset-77", "Weekend cooking reel", "Deliver the 30-second cut with captions by Friday."),
        BuyerUpdate("buyer-8", "Please confirm the Friday delivery."),
    )
    result = handoff_order(request, FakeClient())
    assert result.decision == "handoff"
    assert result.order_id == "order-1042"
    assert "confirmed" in result.buyer_message
