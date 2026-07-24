import pytest
from app.analytics.entropy_calculator import calculate_shannon_entropy
from app.analytics.rto_classifier import RTOClassifier
from app.analytics.inventory_solver import InventorySolver
from app.analytics.margin_optimizer import MarginOptimizer
from app.analytics.returns_verifier import ReturnsVerifier
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shannon_entropy_precision():
    vague_entropy = calculate_shannon_entropy("Riyadh near mosque")
    detailed_entropy = calculate_shannon_entropy("Riyadh, Olaya District, King Fahd Road, Building 45, Floor 3")
    assert detailed_entropy > vague_entropy
    assert vague_entropy >= 0.0

def test_rto_classifier_probability():
    classifier = RTOClassifier()
    low_risk = classifier.predict_rto_probability("Riyadh, Olaya District, King Fahd Road, Building 45, Floor 3", 0)
    high_risk = classifier.predict_rto_probability("Riyadh near mosque", 3)
    assert high_risk > low_risk
    assert 0.0 <= low_risk <= 1.0

def test_api_checkout_route():
    payload = {
        "address_text": "Riyadh near mosque",
        "historical_refusals": 3,
        "email": "test@domain.com"
    }
    response = client.post("/api/v1/checkout/verify-cod", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["payment_suspension"] is True

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

def test_inventory_solver_rop():
    solver = InventorySolver()
    safety_stock = solver.calculate_safety_stock(
        avg_sales=100.0, lead_time_days=5, sales_std_dev=15.0, lead_time_std_dev=1.2
    )
    rop = solver.calculate_reorder_point(avg_sales=100.0, lead_time_days=5, safety_stock=safety_stock)
    
    assert safety_stock > 0
    assert rop == (100.0 * 5) + safety_stock

def test_margin_optimizer_discount():
    optimizer = MarginOptimizer(min_profit_margin_percent=0.20) # 20% margin
    max_discount = optimizer.calculate_max_safe_discount(price=200.0, cogs=100.0, shipping=15.0)
    
    # Target profit: 200.0 * 0.20 = 40.0
    # Max discount: 200.0 - 100.0 - 15.0 - 40.0 = 45.0
    assert max_discount == 45.0
    assert optimizer.evaluate_discount_request(200.0, 100.0, 15.0, 40.0) is True
    assert optimizer.evaluate_discount_request(200.0, 100.0, 15.0, 50.0) is False

def test_returns_verifier_decisions():
    verifier = ReturnsVerifier()
    
    # Happy case: low value, matching weight, correct tags
    pass_case = verifier.evaluate_refund_request(
        item_price=80.0, expected_weight=1.5, scanned_weight=1.51, tag_matched=True, customer_risk_level="Low"
    )
    assert pass_case["decision"] == "APPROVED_INSTANT"
    
    # High value case
    high_val = verifier.evaluate_refund_request(
        item_price=200.0, expected_weight=1.5, scanned_weight=1.51, tag_matched=True, customer_risk_level="Low"
    )
    assert high_val["decision"] == "HELD_FOR_INSPECTION"
    
    # Weight mismatch (swapped item)
    weight_fail = verifier.evaluate_refund_request(
        item_price=80.0, expected_weight=1.5, scanned_weight=1.0, tag_matched=True, customer_risk_level="Low"
    )
    assert weight_fail["decision"] == "HELD_FOR_INSPECTION"
