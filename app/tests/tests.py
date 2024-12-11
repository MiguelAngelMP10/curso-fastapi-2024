from fastapi.testclient import TestClient


def test_client(client):
    print(type(client))
    assert type(client) == TestClient
