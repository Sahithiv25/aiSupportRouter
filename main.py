from ollama import chat

from models import SupportDecision
from tools import (
    create_ticket,
    request_refund_review,
    lookup_order,
    escalate_to_human
)


def analyze_request(customer_message: str) -> SupportDecision:
    response = chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI customer support triage system.

Analyze the customer's request and return a structured decision.

Intent:
- refund_request: refunds, duplicate charges, billing refunds
- account_access: login, password, locked account
- order_status: shipping, delivery, order tracking
- subscription_issue: cancellation, renewal, subscription issue
- general_support: anything else

Priority:
- low: informational/minor
- medium: normal support issue
- high: financial loss, repeated failure, or urgent impact

Risk:
- low: simple informational request
- medium: financial or account issue
- high: sensitive or potentially damaging action

Human approval:
- Refunds require human approval
- High-risk cases require human approval

Recommended action:
- create_ticket
- request_refund_review
- lookup_order
- escalate_to_human

Keep reasoning short.
"""
            },
            {
                "role": "user",
                "content": customer_message
            }
        ],
        format=SupportDecision.model_json_schema(),
        options={"temperature": 0}
    )

    return SupportDecision.model_validate_json(
        response.message.content
    )


def route_action(decision: SupportDecision):

    if decision.recommended_action == "create_ticket":
        return create_ticket()

    elif decision.recommended_action == "request_refund_review":
        return request_refund_review()

    elif decision.recommended_action == "lookup_order":
        return lookup_order()

    elif decision.recommended_action == "escalate_to_human":
        return escalate_to_human()

    else:
        return "No valid action found."


def run_support_router(customer_message: str):

    print("\n--- CUSTOMER REQUEST ---")
    print(customer_message)

    decision = analyze_request(customer_message)

    print("\n--- AI DECISION ---")
    print(f"Intent: {decision.intent}")
    print(f"Priority: {decision.priority}")
    print(f"Amount: {decision.amount}")
    print(f"Risk Level: {decision.risk_level}")
    print(f"Human Approval: {decision.requires_human_approval}")
    print(f"Recommended Action: {decision.recommended_action}")
    print(f"Reasoning: {decision.reasoning}")

    result = route_action(decision)

    print("\n--- TOOL EXECUTION ---")
    print(result)


if __name__ == "__main__":

    customer_message = input(
        "\nEnter customer request: "
    )

    run_support_router(customer_message)