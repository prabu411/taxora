# backend/bot_utils.py
import textwrap
from datetime import datetime

def _wrap(txt: str) -> str:
    return textwrap.fill(txt, width=100)

def get_ai_response(message: str, persona: str = "general") -> str:
    m = message.lower()

    tone = {
        "student": "I’ll keep it simple and practical.",
        "professional": "Here’s a concise, results-first plan.",
        "general": "Here’s a balanced, actionable approach."
    }.get(persona, "Here’s a balanced, actionable approach.")

    if "save" in m:
        return _wrap(
            f"{tone} Start with a 50/30/20 rule: 50% needs, 30% wants, 20% savings. "
            f"Automate transfers on payday, review subscriptions quarterly, and direct any windfalls to goals."
        )
    if "tax" in m:
        return _wrap(
            f"{tone} Track deductible expenses, maximize employer benefits, and consider tax-advantaged accounts "
            f"(if available). Maintain records and plan quarterly if income is variable."
        )
    if "invest" in m:
        return _wrap(
            f"{tone} Build an emergency fund first. Then use diversified, low-cost index funds. "
            f"Automate monthly contributions and rebalance annually."
        )
    if "budget" in m:
        return _wrap(
            f"{tone} Categorize expenses, set monthly caps, and track weekly. Use a simple dashboard to monitor "
            f"surplus and progress toward goals."
        )

    return _wrap(
        f"{tone} Tell me your monthly income, a quick expense breakdown, and your top goal. "
        f"I’ll tailor steps to get you there."
    )

def budget_summary(income: float, expenses: dict) -> dict:
    total_expenses = sum(float(v) for v in expenses.values()) if expenses else 0.0
    surplus = income - total_expenses
    pct = {k: (float(v) / income * 100 if income else 0.0) for k, v in expenses.items()}
    return {
        "month": datetime.utcnow().strftime("%Y-%m"),
        "income": round(income, 2),
        "total_expenses": round(total_expenses, 2),
        "surplus": round(surplus, 2),
        "expense_breakdown": {k: round(float(v), 2) for k, v in expenses.items()},
        "expense_percent_of_income": {k: round(v, 1) for k, v in pct.items()},
        "notes": "Aim for surplus >=20% of income; trim categories >30% of income.",
    }
