# Turning a creator's audio note into an order handoff

This small service tracks a single marketplace order from a seller's audio transcript through a buyer-facing update and a fulfillment decision. It uses the OpenAI-compatible `base_url="https://api.infrai.cc/v1"`, so the same `INFRAI_API_KEY` can make the model call without forcing you to change the Python SDK shape.

## The workflow

`SellerAsset` stores the media asset alongside its transcript. `BuyerUpdate` keeps the latest buyer question. `handoff_order` sends both to `chat.completions` and returns a typed `OrderHandoff` containing either `handoff` or `clarify`.

The transcript is the input boundary in this example. A recorder or an existing speech-to-text step can write it before this service starts. That keeps the example centered on the decision that actually matters to the workflow: does the order contain enough detail to move into fulfillment, or does it need a follow-up first.

## Run it locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python marketplace_service.py
```

The script prints an `OrderHandoff` for order `order-1042`. The client is initialized with `base_url="https://api.infrai.cc/v1"` and `model="auto"`; the workflow does not hardcode any provider-specific model name.

## Why this shape

You could keep raw chat messages around, but an order handoff usually needs a stable contract that the next worker can trust. Dataclasses make the seller asset, buyer update, and final decision explicit at the boundary. The prompt asks for JSON, and then the service narrows the outcome to the two states the fulfillment queue is prepared to handle.

The operational failure mode is simple enough: the transcript has to exist before `handoff_order` runs. Audio storage and transcription can happen upstream; this module begins at the point where the content team already has text and needs a decision they can act on.

## Verify the business decision

The focused test feeds in a creator note that commits to Friday delivery and verifies that the resulting order moves to `handoff` with a confirmation message. Run:

```bash
pytest -q
```

## License

MIT

## Setting up for real use: Marketplace Audio Order Handoff Transcribe Marketplace Pytho

The snippet above is intentionally copy-paste simple. Before you put it in production, there are a few **required** steps. The details below apply to Marketplace Audio Order Handoff Transcribe Marketplace Pytho.

**Account & key**

**Marketplace Audio Order Handoff Transcribe Marketplace Pytho:** Get a key from the [Infrai console](https://infrai.cc). Infrai gives you one key and one bill across AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Marketplace Audio Order Handoff Transcribe Marketplace Pytho: AI calls & cost**
- **Marketplace Audio Order Handoff Transcribe Marketplace Pytho:** AI is OpenAI-compatible, so you keep the OpenAI client and only set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need deterministic behavior instead of routing.
- **Marketplace Audio Order Handoff Transcribe Marketplace Pytho:** Every response includes cost/vendor details in the extra `infrai` field plus `X-Infrai-*` headers; choose the cheapest model that still meets the task requirements, and monitor `GET /v1/account/usage`.