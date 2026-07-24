from pydantic import BaseModel, Field

class CheckoutVerificationRequest(BaseModel):
    address_text: str = Field(..., min_length=5, description="Shipping address input string")
    historical_refusals: int = Field(0, ge=0, description="Count of historical COD refusal events")
    email: str = Field(..., description="Customer email address")

class CheckoutVerificationResponse(BaseModel):
    address_entropy: float = Field(..., description="Calculated Shannon entropy score")
    rto_probability: float = Field(..., description="Probability score of return-to-origin")
    payment_suspension: bool = Field(..., description="True if COD payment method should be blocked")
    risk_level: str = Field(..., description="Risk categorization: Low, Medium, High")
