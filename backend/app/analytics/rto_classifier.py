import math
from .entropy_calculator import calculate_shannon_entropy

class RTOClassifier:
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        # Coefficients derived from calibrating historical GCC logistics data
        self.beta_0 = 0.5         # Intercept
        self.beta_entropy = -0.85 # Higher entropy (better address) decreases RTO risk
        self.beta_refusals = 1.25 # More previous refusals increase RTO risk

    def predict_rto_probability(self, address_text: str, historical_refusals: int) -> float:
        """
        Calculates the probability of delivery failure (RTO) using a logistic function:
        P(RTO) = 1 / (1 + e^-(beta_0 + beta_entropy * Entropy + beta_refusals * Refusals))
        """
        entropy = calculate_shannon_entropy(address_text)
        
        # Calculate raw logit
        logit = self.beta_0 + (self.beta_entropy * entropy) + (self.beta_refusals * historical_refusals)
        
        # Sigmoid activation
        probability = 1.0 / (1.0 + math.exp(-logit))
        return round(probability, 4)
