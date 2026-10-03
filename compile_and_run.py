import os
import torch
import torch.nn as nn
from decimal import Decimal
from huggingface_hub import hf_hub_download
from engine.client import ResilientAIEngine

# --- 1. PyTorch Model Definition (matches Kaggle training architecture) ---
class StoreDemandForecaster(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=128, num_layers=2, output_dim=12):
        super(StoreDemandForecaster, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2,
            bidirectional=True
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_step = lstm_out[:, -1, :]
        return self.fc(last_step)

def execute_compiled_pipeline():
    print("=" * 65)
    print("EXECUTING COMPILED ENTERPRISE PIPELINE: KAGGLE ML + CODESPACES")
    print("=" * 65)

    # 2. Initialize Model
    model = StoreDemandForecaster(input_dim=1, hidden_dim=128, num_layers=2, output_dim=12)
    weights_path = "sbux_demand_bilstm.pt"

    if not os.path.exists(weights_path):
        try:
            print("Fetching trained weights from Hugging Face Registry...")
            weights_path = hf_hub_download(
                repo_id="amityoshops-dev/sbux-demand-engine",
                filename="sbux_demand_bilstm.pt"
            )
            print(f"Loaded weights from: {weights_path}")
            model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
        except Exception as e:
            print(f"[Notice] Remote fetch note: {e}. Executing architecture directly.")
    else:
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))

    model.eval()

    # 3. Execute Shift Demand Inference
    print("\n[Stage 1/2] Computing 12-Hour Store Shift Demand...")
    mock_hourly_history = torch.randn(1, 72, 1) # 72-hour sliding window
    with torch.no_grad():
        forecast = model(mock_hourly_history).numpy()[0]

    forecasted_cups = [max(10.0, round(float(f) + 50.0, 1)) for f in forecast]
    total_cups = sum(forecasted_cups)
    milk_liters = round(total_cups * 0.22, 1)
    beans_kg = round(total_cups * 0.018, 1)

    print(f"-> 12-Hour Cup Forecast: {total_cups:.1f} units")
    print(f"-> Required Dairy Replenishment: {milk_liters} Liters")
    print(f"-> Required Coorg Bean Allocation: {beans_kg} kg")

    # 4. Execute Financial Settlement Audit
    print("\n[Stage 2/2] Running POS vs Settlement Reconciliation...")
    audit_payload = {
        "store_id": "SBUX_PUNE_FC01",
        "predicted_shift_volume_cups": total_cups,
        "material_needs": {"milk_liters": milk_liters, "beans_kg": beans_kg},
        "pos_gross_sales": 2365.00,
        "cleared_cash": 1815.00,
        "unreconciled_leakage": 550.00,
        "issues": ["TXN_102: MDR Under-settled ₹40", "TXN_103: Asynchronous UPI ₹395", "TXN_104: Wallet Sync Drop ₹510"]
    }

    # 5. Executive AI Decision Directive
    ai_engine = ResilientAIEngine()
    
    prompt = (
        "You are acting as Managing Director / Chief Operating Officer on behalf of Intent Curiosity Sphere (ICS) Retail Research Lab.\n"
        "Review this integrated operational telemetry output:\n"
        f"{audit_payload}\n\n"
        "Generate a concise, 4-point C-Suite action order:\n"
        "1. Shift Production & Barista Allocation\n"
        "2. Automated Dairy & Coffee bean replenishment purchase order\n"
        "3. Immediate banking dispute & nodal settlement resolution\n"
        "4. Store Manager accountability directive\n\n"
        "Sign and format the conclusion strictly as:\n"
        "Execute now.\n\n"
        "Intent Curiosity Sphere (ICS)\n"
        "Retail & FinTech Architecture Lab\n\n"
        "---\n"
        "DISCLAIMER:\n"
        "This document, analysis, and operational directive represent independent educational research and technical simulation models developed by Intent Curiosity Sphere (ICS). This case study is conducted strictly for educational, analytical, and architectural modeling purposes and does not represent official company policy, internal corporate records, or endorsements by Tata Starbucks Private Limited, Starbucks Corporation, or Tata Consumer Products."
    )

    directive = ai_engine.execute_prompt(
        system_prompt="You are an enterprise retail Chief Operating Officer and financial systems architect.",
        user_prompt=prompt
    )

    print("\n" + "=" * 65)
    print("COMPILED EXECUTIVE DISPATCH:")
    print("=" * 65)
    print(directive)
    print("=" * 65)

if __name__ == "__main__":
    execute_compiled_pipeline()
