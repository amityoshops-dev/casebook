import sys
from engine.client import ResilientAIEngine

def main():
    print("Initializing Resilient AI Engine...\n")
    engine = ResilientAIEngine()

    system_role = (
        "You are an enterprise fintech and transaction systems architect. "
        "Provide direct, concise, production-ready specifications."
    )
    user_task = "List 3 essential validation checks for an ISO 20022 pacs.008 customer credit transfer payload."

    print(f"Task: {user_task}\n")
    output = engine.execute_prompt(system_role, user_task)

    print("-" * 50)
    print("Engine Response:\n")
    print(output)
    print("-" * 50)

if __name__ == "__main__":
    main()
