import pytest
from app.analytics.entropy_calculator import calculate_shannon_entropy
from app.analytics.rto_classifier import RTOClassifier
from app.api.endpoints import router
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shannon_entropy_precision():
    # Vague short address
    vague_entropy = calculate_shannon_entropy("Riyadh near mosque")
    # Highly structured detailed address
    detailed_entropy = calculate_shannon_entropy("Riyadh, Olaya District, King Fahd Road, Building 45, Floor 3")
    
    assert detailed_entropy > vague_entropy
    assert vague_entropy >= 0.0

def test_rto_classifier_probability():
    classifier = RTOClassifier()
    
    # Low risk parameters
    low_risk = classifier.predict_rto_probability("Riyadh, Olaya District, King Fahd Road, Building 45, Floor 3", 0)
    # High risk parameters
    high_risk = classifier.predict_rto_probability("Riyadh near mosque", 3)
    
    assert high_risk > low_risk
    assert 0.0 <= low_risk <= 1.0
    assert 0.0 <= high_risk <= 1.0

def test_api_checkout_route():
    payload = {
        "address_text": "Riyadh near mosque",
        "historical_refusals": 3,
        "email": "test@domain.com"
    }
    response = client.post("/api/v1/checkout/verify-cod", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "rto_probability" in data
    assert data["payment_suspension"] is True  # High risk should block COD

def test_api_whatsapp_webhook():
    payload = {
        "location": {
            "latitude": 24.7136,
            "longitude": 46.6753
        }
    }
    response = client.post("/api/v1/whatsapp/webhook", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "coordinate" in data["message"]
