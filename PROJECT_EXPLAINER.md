# 📖 Project Explainer: OmniPulse Multi-Agent E-Commerce Optimizer

This document provides a detailed breakdown of the mathematical models, algorithmic designs, security controls, and MLOps structures powering **OmniPulse**.

---

## 1. Mathematical Algorithms

### A. Shannon Entropy (Address Clarity Check)
To analyze if a checkout shipping address is vague (e.g. *"Riyadh, near supermarket"*) or detailed/structured (e.g. *"Riyadh, Olaya District, King Fahd Rd, Building 12, Floor 3"*), we calculate the **Shannon Entropy** of the text words:

$$E = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

*   **Vague short addresses** result in a very low entropy score.
*   **Highly structured addresses** have diverse word types, resulting in a high entropy score.
*   **The Adjustment**: We apply a length penalty multiplier to penalize ultra-short text strings.

### B. Logistic Probability Risk Scoring
To evaluate the RTO (Return to Origin) risk level of an order, we pass the entropy score and customer history parameters into a logistic function:

$$P_{\text{RTO}} = \frac{1}{1 + e^{-(\beta_0 + \beta_1 \cdot E_{\text{address}} + \beta_2 \cdot H_{\text{refusals}})}}$$

*   $\beta_1 = -0.85$ (As address entropy increases, the risk of a failed delivery decreases).
*   $\beta_2 = 1.25$ (Each historical refusal significantly increases the risk score).
*   **Decision Rule**: If $P_{\text{RTO}} \ge 0.35$ (35% risk threshold), the system automatically hides the Cash on Delivery (COD) option, mitigating courier returns and shipping costs.

---

## 2. Automated Swarms (Multi-Agent System)

1.  **Checkout Risk Agent**: Evaluates the order payload, calculates entropy, and restricts COD payments dynamically.
2.  **Exit-Intent Chatbot**: Monitors user mouse movements. If they move their cursor outside the top viewport window (exit-intent), the AI agent evaluates product profit margins. If the margin permits, it generates a custom 10% discount code (**INDIGO10**) and displays it in the chat interface.
3.  **Returns Inspector (Computer Vision)**: Inspects returned items automatically. By running semantic segmentation on tag positions and checking package weight discrepancies, the system flags return fraud (such as "pebble-swapping" or empty package scams).

---

## 3. MLOps & System Telemetry

To ensure system reliability in production:
*   **Kubernetes Scaling (KEDA)**: Auto-scales the processing pods based on incoming checkout volume. During sales events (e.g. Ramadan, White Friday), pods scale from 1 to 8 workers, scaling back down to 1 when idle.
*   **Data Drift (KS-Stat)**: Tracks incoming address statistics. If customers start using new abbreviations, the KS-Statistic drifts, triggering an MLflow model retrain.
*   **Security (WAF logs)**: Blocks malicious IP vectors attempting to lock up store inventory by placing mock fake COD orders.
