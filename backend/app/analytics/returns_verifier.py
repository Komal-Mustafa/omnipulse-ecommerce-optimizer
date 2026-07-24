class ReturnsVerifier:
    def __init__(self, high_value_threshold: float = 150.0):
        self.val_threshold = high_value_threshold

    def evaluate_refund_request(self, item_price: float, expected_weight: float, scanned_weight: float, tag_matched: bool, customer_risk_level: str) -> dict:
        """
        Consensus Refund Decision logic matching physical weight bounds and customer tiers.
        High value items or high risk clients require physical inspection (no instant refunds).
        """
        weight_discrepancy = abs(expected_weight - scanned_weight)
        weight_passed = weight_discrepancy <= 0.05 # Allow maximum 50g tolerance
        
        decision = "APPROVED_INSTANT"
        status_message = "Scan validated. Refund approved and issued automatically."
        
        if not tag_matched:
            decision = "REJECTED_FRAUD"
            status_message = "Tag verification failed. Fraud flagged."
        elif not weight_passed:
            decision = "HELD_FOR_INSPECTION"
            status_message = "Weight discrepancy detected. Package locked for manual inspection."
        elif item_price >= self.val_threshold:
            decision = "HELD_FOR_INSPECTION"
            status_message = "High-value item returns require physical inspection before payout."
        elif customer_risk_level == "High":
            decision = "HELD_FOR_INSPECTION"
            status_message = "High risk profile account returns require manual check verification."
            
        return {
            "decision": decision,
            "weight_discrepancy": round(weight_discrepancy, 3),
            "status_message": status_message
        }
