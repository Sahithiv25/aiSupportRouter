from ollama import chat

from models import SupportDecision


def analyze_request(customer_message: str) -> SupportDecision:
    response = chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI customer support triage system.

Analyze the customer's request and return a structured decision.

Rules:

Intent:
- refund_request: refunds, duplicate charges, billing refunds
- account_access: login, password, locked account
- order_status: shipping, delivery, order tracking
- subscription_issue: cancellation, renewal, subscription problem
- general_support: anything else

Priority:
- low: informational or minor issue
- medium: normal support issue
- high: financial loss, repeated failure, or urgent impact

Risk:
- low: simple informational request
- medium: financial or account-related issue
- high: sensitive or potentially damaging action

Human approval:
- Refunds require human approval.
- High-risk cases require human approval.

Recommended action:
Choose exactly one:
- create_ticket
- request_refund_review
- lookup_order
- escalate_to_human

Return the result as JSON matching the required schema.
Keep reasoning short.
"""
            },
            {
                "role": "user",
                "content": customer_message
            }
        ],

        # THIS is the structured-output part
        format=SupportDecision.model_json_schema(),

        # Makes the response more deterministic
        options={
            "temperature": 0
        }
    )

    # Convert returned JSON into our validated Pydantic object
    decision = SupportDecision.model_validate_json(
        response.message.content
    )

    return decision


if __name__ == "__main__":

    customer_message = """
    I was charged twice for my order.
    Each charge was $84 and I want my money back.
    """

    decision = analyze_request(customer_message)

    print("\n--- CUSTOMER REQUEST ---")
    print(customer_message.strip())

    print("\n--- SUPPORT DECISION ---")
    print(f"Intent: {decision.intent}")
    print(f"Priority: {decision.priority}")
    print(f"Amount: {decision.amount}")
    print(f"Risk Level: {decision.risk_level}")
    print(
        f"Human Approval: "
        f"{decision.requires_human_approval}"
    )
    print(
        f"Recommended Action: "
        f"{decision.recommended_action}"
    )
    print(f"Reasoning: {decision.reasoning}")