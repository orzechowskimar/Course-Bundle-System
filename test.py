from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_calculate_quotes():
    request_data = {
        "topics": {
            "reading": 20,
            "math": 50,
            "science": 30,
            "history": 15,
            "art": 10
        }
    }
    provider_data = {
        "provider_topics": {
            "provider_a": "math+science",
            "provider_b": "reading+science",
            "provider_c": "history+math"
        }
    }
    response = client.post("/calculate_quotes/", json={
        "topics": request_data["topics"],
        "provider_topics": provider_data["provider_topics"]
    })
    assert response.status_code == 200
    assert response.json() == {
        "quotes": {
            "provider_a": 8.0,
            "provider_b": 5.0,
            "provider_c": 12.5
        }
    }
