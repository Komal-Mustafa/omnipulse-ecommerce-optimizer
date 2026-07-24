class InventorySolver:
    def __init__(self, service_level_factor: float = 1.65):
        # service_level_factor 1.65 matches a 95% service level standard
        self.k = service_level_factor

    def calculate_safety_stock(self, avg_sales: float, lead_time_days: int, sales_std_dev: float, lead_time_std_dev: float) -> float:
        """
        Calculates safety stock under demand and lead time uncertainty:
        Safety Stock = k * sqrt(LeadTime * SalesStdDev^2 + Sales^2 * LeadTimeStdDev^2)
        """
        term1 = lead_time_days * (sales_std_dev ** 2)
        term2 = (avg_sales ** 2) * (lead_time_std_dev ** 2)
        safety_stock = self.k * (term1 + term2) ** 0.5
        return round(safety_stock, 2)

    def calculate_reorder_point(self, avg_sales: float, lead_time_days: int, safety_stock: float) -> float:
        """
        Calculates Reorder Point (ROP):
        ROP = (Average Daily Sales * Lead Time) + Safety Stock
        """
        rop = (avg_sales * lead_time_days) + safety_stock
        return round(rop, 2)
