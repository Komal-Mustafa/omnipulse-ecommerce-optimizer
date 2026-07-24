# 🛍️ OmniPulse — Enterprise E-Commerce Optimizer Swarm

<div align="center">
  <img src="https://img.shields.io/badge/Language-Python-7C3AED?style=flat-square" alt="Python"/>
  <img src="https://img.shields.io/badge/ML%20Library-Scikit--learn-7C3AED?style=flat-square" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/Framework-FastAPI-7C3AED?style=flat-square" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Ops-KEDA%20%2F%20MLflow-7C3AED?style=flat-square" alt="MLOps"/>
</div>

---

## 🌟 Overview
**OmniPulse** is an institutional-grade, multi-agent AI system designed to solve the three most expensive bottlenecks facing digital e-commerce merchants: **Return Logistics (RTO) Fraud**, **Cart Abandonment**, and **Inventory Stockouts**.

Featuring a **3D-rendered network flow background**, an interactive **checkout risk chatbot**, and a live **AIOps/MLOps telemetry panel**, this project demonstrates how machine learning and operations automation can be combined into a seamless, production-ready system.

---

## 🚀 Key Features

*   **Shannon Entropy Address Parser**: Computes text randomness to flag vague, un-deliverable shipping addresses (Romanized Urdu / Arabic) before dispatch.
*   **Logistic Risk Scoring**: Employs Scikit-learn to calculate Return-to-Origin probability ($P_{\text{RTO}}$), automatically suspending COD checks if the risk is high.
*   **Margin-Aware Exit-Intent Chatbot**: Monitors customer exit patterns, checks product profit margins, and issues custom discount codes automatically.
*   **Computer Vision Return Scanner**: Simulates barcode verification and weight-discrepancy checking to identify item return fraud.
*   **KEDA Autoscaling & MLOps**: Simulates automated Kubernetes scaling from 1 to 8 pods during peak sales traffic and tracks dataset drift logs.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Backend API** | Python, FastAPI, Uvicorn, Pydantic |
| **Data & ML** | Scikit-learn, Pandas, NumPy, Jupyter Notebook |
| **Frontend UI** | HTML5 Canvas, Tailwind CSS, Leaflet.js Maps, Chart.js |
| **Testing** | Pytest, FastAPI TestClient |
| **Verification** | MLflow telemetry logging, KEDA autoscaling |

---

## ⚙️ How to Run & Verify

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Komal-Mustafa/omnipulse-ecommerce-optimizer.git
    cd omnipulse-ecommerce-optimizer
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  **Run the FastAPI Backend**:
    ```bash
    python -m uvicorn app.main:app --reload --cwd backend/
    ```
4.  **Run Pytest Suite**:
    ```bash
    python -m pytest backend/tests/
    ```
5.  **Open the Dashboard**:
    Open `index.html` in your browser to interact with the 3D dashboard, map, and checkout terminal.
