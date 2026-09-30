from pydantic import BaseModel
from typing import Literal, Optional

class SupportDecision(BaseModel):
    intent: Literal[
        "refund_request",
        "account_access",
        "order_status",
        "subscription_issue",
        "general_support"
    ]


    priority: Literal["low", "medium", "high"]

    amount: Optional[float] = None

    risk_level: Literal["low", "medium", "high"]

    requires_human_approval: bool

    recommended_action: Literal[
        "create_ticket",
        "request_refund_review",
        "lookup_order",
        "escalate_to_human"
    ]

    reasoning: str

# Instead of the model giving a prose, this forces it into a known schema