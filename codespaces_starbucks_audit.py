import json
from decimal import Decimal
from dataclasses import dataclass
from typing import List, Dict

# Uses the ResilientAIEngine we created earlier in engine/client.py
from engine.client import ResilientAIEngine

@dataclass
class POSReceipt:
    transaction_id: str
    store_id: str
    timestamp: str
    item_summary: str
    gross_amount: Decimal
    payment_method: str

@dataclass
class SettlementRecord:
    transaction_id: str
    cleared_amount: Decimal
    mdr_fee: Decimal
    status: str

class StarbucksStoreAuditor:
    def __init__(self, store_id: str):
        self.store_id = store_id
        self.ai_engine = ResilientAIEngine()

    def run_reconciliation(self, pos_sales: List[POSReceipt], settlements: Dict[str, SettlementRecord]):
        print(f"\n========================================================")
        print(f"RUNNING RECONCILIATION FOR STORE: {self.store_id}")
        print(f"========================================================")
        matched = 0
        discrepancies = []

        for sale in pos_sales:
            settlement = settlements.get(sale.transaction_id)
            if not settlement:
                discrepancies.append({
                    "tx_id": sale.transaction_id,
                    "issue": "MISSING_SETTLEMENT",
                    "expected": float(sale.gross_amount),
                    "cleared": 0.0,
                    "payment_method": sale.payment_method
                })
            elif settlement.cleared_amount != sale.gross_amount:
                discrepancies.append({
                    "tx_id": sale.transaction_id,
                    "issue": "AMOUNT_MISMATCH",
                    "expected": float(sale.gross_amount),
                    "cleared": float(settlement.cleared_amount),
                    "difference": float(sale.gross_amount - settlement.cleared_amount),
                    "payment_method": sale.payment_method
                })
            elif settlement.status != "SUCCESS":
                discrepancies.append({
                    "tx_id": sale.transaction_id,
                    "issue": f"GATEWAY_STATUS_{settlement.status}",
                    "expected": float(sale.gross_amount),
                    "cleared": float(settlement.cleared_amount),
                    "payment_method": sale.payment_method
                })
            else:
                matched += 1

        print(f"Matched & Cleared Transactions : {matched}")
        print(f"Exceptions / Discrepancies Found: {len(discrepancies)}")

        if discrepancies:
            print("\nDispatching discrepancies to Resilient AI Engine for Executive Audit...")
            prompt = (
                f"You are the Chief Financial Controller for Tata Starbucks India.\n"
                f"Analyze the following transactional settlement exceptions for Store {self.store_id} "
                f"and provide an actionable audit root-cause memorandum covering UPI, Card MDR, and Wallet reconciliation:\n"
                f"{json.dumps(discrepancies, indent=2)}"
            )
            memo = self.ai_engine.execute_prompt(
                system_prompt="You are an enterprise financial controller and transactional systems auditor.",
                user_prompt=prompt
            )
            print("\n---------------- EXECUTIVE AUDIT MEMO ----------------")
            print(memo)
            print("------------------------------------------------------")

if __name__ == "__main__":
    # Test Data: Shift POS Sales vs Gateway Settlements
    mock_pos = [
        POSReceipt("TXN_101", "SBUX_PUNE_FC01", "10:14:02", "1x Venti Latte, 1x Croissant", Decimal("620.00"), "UPI"),
        POSReceipt("TXN_102", "SBUX_PUNE_FC01", "10:15:30", "2x Grande Frappuccino", Decimal("840.00"), "CARD"),
        POSReceipt("TXN_103", "SBUX_PUNE_FC01", "10:18:11", "1x Flat White (Oat Milk)", Decimal("395.00"), "UPI"),
        POSReceipt("TXN_104", "SBUX_PUNE_FC01", "10:22:45", "1x Cold Brew, 1x Muffin", Decimal("510.00"), "STARBUCKS_CARD"),
    ]

    mock_settlements = {
        "TXN_101": SettlementRecord("TXN_101", Decimal("620.00"), Decimal("0.00"), "SUCCESS"),
        "TXN_102": SettlementRecord("TXN_102", Decimal("800.00"), Decimal("16.80"), "SUCCESS"),  # Amount mismatch (₹40 under-cleared)
        "TXN_103": SettlementRecord("TXN_103", Decimal("395.00"), Decimal("0.00"), "FAILED"),    # Gateway fail
        # TXN_104 is missing settlement (unsettled wallet sync delay)
    }

    auditor = StarbucksStoreAuditor(store_id="SBUX_PUNE_FC01")
    auditor.run_reconciliation(mock_pos, mock_settlements)
