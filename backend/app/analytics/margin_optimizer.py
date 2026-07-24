class MarginOptimizer:
    def __init__(self, min_profit_margin_percent: float = 0.15):
        self.min_margin = min_profit_margin_percent

    def calculate_max_safe_discount(self, price: float, cogs: float, shipping: float) -> float:
        """
        Calculates maximum discount keeping profit margin above target limits:
        Max Discount = Price - COGS - Shipping - Target Profit
        Where: Target Profit = Price * min_profit_margin_percent
        """
        target_profit = price * self.min_margin
        max_discount = price - cogs - shipping - target_profit
        
        # Return discount, clamped to 0 if margins are negative
        return max(0.0, round(max_discount, 2))

    def evaluate_discount_request(self, price: float, cogs: float, shipping: float, requested_discount: float) -> bool:
        """
        Checks if the requested discount satisfies target margin constraints.
        """
        max_safe = self.calculate_max_safe_discount(price, cogs, shipping)
        return requested_discount <= max_safe
