from fastapi import APIRouter, HTTPException
from ..models.schemas import CheckoutVerificationRequest, CheckoutVerificationResponse
from ..analytics.rto_classifier import RTOClassifier
from ..analytics.entropy_calculator import calculate_shannon_entropy

router = APIRouter()
classifier = RTOClassifier()

@router.post("/checkout/verify-cod", response_model=CheckoutVerificationResponse)
async def verify_cod_checkout(payload: CheckoutVerificationRequest):
    try:
        entropy = calculate_shannon_entropy(payload.address_text)
        prob = classifier.predict_rto_probability(payload.address_text, payload.historical_refusals)
        
        # Suspend COD if RTO probability is equal to or greater than 35%
        suspension = prob >= 0.35
        
        risk_level = "Low"
        if prob >= 0.65:
            risk_level = "High"
        elif prob >= 0.35:
            risk_level = "Medium"
            
        return CheckoutVerificationResponse(
            address_entropy=round(entropy, 4),
            rto_probability=prob,
            payment_suspension=suspension,
            risk_level=risk_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/whatsapp/webhook")
async def receive_whatsapp_webhook(payload: dict):
    # Simulates receiving coordinates location pin
    location = payload.get("location", {})
    lat = location.get("latitude")
    lon = location.get("longitude")
    
    if not lat or not lon:
        return {"status": "error", "message": "Missing coordinate data"}
        
    return {
        "status": "success",
        "message": f"Successfully registered coordinate anchor points: Lat {lat}, Lon {lon}"
    }
