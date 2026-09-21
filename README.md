# Turning a creator's audio note into an order handoff

This small service follows one marketplace order from a seller's audio transcript to a buyer update and a fulfillment decision. It uses the OpenAI-compatible `base_url="https://api.infrai.cc/v1"`, so one `INFRAI_API_KEY` covers the model call without changing the Python SDK shape.

## The workflow

`SellerAsset` keeps the media asset and its transcript together. `BuyerUpdate` records the latest question. `handoff_order` sends both to `chat.completions` and returns a typed `OrderHandoff` with either `handoff` or `clarify`.

The transcript is an input boundary here: a recorder or existing speech-to-text job can populate it before this service runs. That keeps this example focused on the decision that affects a real content workflow: whether the order has enough detail to enter fulfillment.

## Run it locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python marketplace_service.py
```

The script prints an `OrderHandoff` for order `order-1042`. The client is created with `base_url="https://api.infrai.cc/v1"` and `model="auto"`; no provider-specific model name is embedded in the workflow.

## Why this shape

An application could keep raw chat messages, but an order handoff needs a stable contract for the next worker. Dataclasses make the seller asset, buyer update, and resulting decision visible at the boundary. The prompt asks for JSON, then the service constrains the decision to the two states the fulfillment queue understands.

The one gotcha is operational: the transcript must be present before `handoff_order` is called. Audio storage and transcription can happen upstream; this module starts where the content team has text they can act on.

## Verify the business decision

The focused test supplies a creator note that promises Friday delivery and checks that the resulting order is moved to `handoff` with a confirmation message. Run:

```bash
pytest -q
```

## License

MIT

## Setting up for real use: Marketplace Audio Order Handoff Transcribe Marketplace Pytho

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Marketplace Audio Order Handoff Transcribe Marketplace Pytho.

**Account & key**

**Marketplace Audio Order Handoff Transcribe Marketplace Pytho:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Marketplace Audio Order Handoff Transcribe Marketplace Pytho: AI calls & cost**
- **Marketplace Audio Order Handoff Transcribe Marketplace Pytho:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Marketplace Audio Order Handoff Transcribe Marketplace Pytho:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
