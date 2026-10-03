import json
from decimal import Decimal
from engine.client import ResilientAIEngine

def build_executive_dispatch():
    # 1. Feed outputs from Kaggle Deep Learning Forecast
    kaggle_shift_forecast = {
        "shift_hours": 12,
        "total_cups_forecasted": 676.4,
        "hourly_breakdown": [64.0, 64.6, 64.1, 63.0, 62.5, 60.8, 57.7, 53.9, 51.2, 48.6, 46.2, 43.9],
        "milk_consumption_liters_est": round(676.4 * 0.22, 1), # ~220ml milk per beverage
        "coffee_beans_kg_est": round(676.4 * 0.018, 1)         # ~18g per double shot
    }

    # 2. Feed financial settlement exceptions from Store Auditor
    audit_exceptions = {
        "store_id": "SBUX_PUNE_FC01",
        "gross_pos_sales": 2365.00,
        "cleared_cash": 1815.00,
        "unreconciled_leakage": 550.00,
        "exception_summary": [
            {"txn": "TXN_102", "type": "MDR_MISCALCULATION", "amount": 40.00},
            {"txn": "TXN_103", "type": "ASYNC_UPI_CLEARING", "amount": 395.00},
            {"txn": "TXN_104", "type": "INTERNAL_WALLET_SYNC_DELAY", "amount": 510.00}
        ]
    }

    print("\nSynthesizing Kaggle DL Forecast & Financial Audit via Executive AI...")

    prompt = f"""
You are the Managing Director & Chief Operating Officer of Tata Starbucks India.
Review the operational telemetry for Store SBUX_PUNE_FC01:

1. KAGGLE 12-HOUR DEMAND INFERENCE:
- Total Projected Demand: {kaggle_shift_forecast['total_cups_forecasted']} cups
- Estimated Raw Material Needs: {kaggle_shift_forecast['milk_consumption_liters_est']} L Milk | {kaggle_shift_forecast['coffee_beans_kg_est']} kg Roasted Espresso Beans

2. FINANCIAL CLEARING & SETTLEMENT LEAKAGE:
- POS Gross Revenue: ₹{audit_exceptions['gross_pos_sales']}
- Settled Funds: ₹{audit_exceptions['cleared_cash']}
- Unreconciled / Float at Risk: ₹{audit_exceptions['unreconciled_leakage']}

DELIVERABLES:
1. Executive Shift Operating Memo (Concise operational directives for Store Manager & Supply Chain Lead).
2. Dynamic Par-Level Reorder: Exact purchase orders to trigger for Coorg beans and local dairy.
3. Liquidity & Audit Directives: Instructions for merchant acquirer settlement dispute.
"""

    engine = ResilientAIEngine()
    result = engine.execute_prompt(
        system_prompt="You are an enterprise COO and retail operations director. Provide sharp, executive-level directives without fluff.",
        user_prompt=prompt
    )

    print("\n" + "=" * 65)
    print("      TATA STARBUCKS OPERATIONAL DISPATCH & P&L DIRECTIVE")
    print("=" * 65)
    print(result)
    print("=" * 65)

if __name__ == "__main__":
    build_executive_dispatch()
