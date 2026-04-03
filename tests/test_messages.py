from uuid import UUID, uuid4

from tests.conftest import TEST_API_KEY

HEADERS = {"X-API-Key": TEST_API_KEY}

MESSAGE_ID = UUID("00000000-0000-0000-0000-000000000001")
CHAT_ID = UUID("00000000-0000-0000-0000-000000000002")

PAYLOAD = {
    "message_id": str(MESSAGE_ID),
    "chat_id": str(CHAT_ID),
    "content": "Hello",
    "rating": True,
    "sent_at": "2026-04-03T09:00:00Z",
    "role": "user",
}


async def test_create_message(client):
    r = await client.post("/messages", json=PAYLOAD, headers=HEADERS)
    assert r.status_code == 201
    assert r.json()["content"] == "Hello"
    assert r.json()["role"] == "user"


async def test_list_messages(client):
    await client.post("/messages", json=PAYLOAD, headers=HEADERS)
    r = await client.get("/messages", headers=HEADERS)
    assert r.status_code == 200
    assert len(r.json()) == 1


async def test_update_message(client):
    await client.post("/messages", json=PAYLOAD, headers=HEADERS)
    r = await client.patch(
        f"/messages/{MESSAGE_ID}",
        json={"content": "Updated", "rating": False},
        headers=HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["content"] == "Updated"
    assert r.json()["rating"] is False


async def test_update_message_not_found(client):
    r = await client.patch(
        f"/messages/{uuid4()}",
        json={"content": "Updated"},
        headers=HEADERS,
    )
    assert r.status_code == 404


async def test_missing_api_key(client):
    r = await client.post("/messages", json=PAYLOAD)
    assert r.status_code == 403


async def test_wrong_api_key(client):
    r = await client.post("/messages", json=PAYLOAD, headers={"X-API-Key": "wrong"})
    assert r.status_code == 403


async def test_list_messages_pagination(client):
    # seed 3 messages with distinct IDs and ascending sent_at so ORDER BY is exercised
    ids = [f"00000000-0000-0000-0000-00000000000{i}" for i in range(1, 4)]
    for i, msg_id in enumerate(ids):
        payload = {**PAYLOAD, "message_id": msg_id, "sent_at": f"2026-04-03T09:0{i}:00Z"}
        await client.post("/messages", json=payload, headers=HEADERS)

    # skip=1, limit=1 → second-oldest message
    r = await client.get("/messages?skip=1&limit=1", headers=HEADERS)
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["message_id"] == ids[1]

    # skip=0, limit=2 → two oldest messages in chronological order
    r = await client.get("/messages?skip=0&limit=2", headers=HEADERS)
    assert r.status_code == 200
    assert [m["message_id"] for m in r.json()] == ids[:2]
