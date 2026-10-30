
def categorize_ticket(text):
    """Assign a support category using predefined keywords."""
    text = text.lower()

    rules = [
        (
            "Security & Privacy",
            [
                "security breach",
                "data breach",
                "unauthorized access",
                "compromised account",
                "suspicious login",
                "stolen data",
                "ransomware",
            ],
        ),
        (
            "Billing & Payments",
            [
                "invoice",
                "billing",
                "charged",
                "charge",
                "refund",
                "payment",
                "subscription fee",
                "overcharged",
            ],
        ),
        (
            "Account Access",
            [
                "locked out",
                "can't log in",
                "cannot log in",
                "can't access",
                "cannot access",
                "unable to sign in",
                "password",
                "login",
                "log in",
                "sign in",
                "account access",
                "access to customer records",
            ],
        ),
        (
            "Technical Issue",
            [
                "bug",
                "error",
                "crash",
                "broken",
                "not working",
                "slow",
                "outage",
                "system down",
                "system is down",
                "timeout",
                "keeps failing",
            ],
        ),
        (
            "Feature Request",
            [
                "feature request",
                "request a feature",
                "would like to add",
                "could you add",
                "feature suggestion",
                "enhancement",
                "product suggestion",
            ],
        ),
    ]

    for category, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return category

    return "General Inquiry"


def prioritize_ticket(text, category):
    """Recommend a priority based on urgency and business impact."""
    text = text.lower()

    security_signals = [
        "security breach",
        "data breach",
        "unauthorized access",
        "compromised account",
        "suspicious login",
        "stolen data",
        "ransomware",
    ]

    widespread_impact = [
        "entire team",
        "whole team",
        "all users",
        "everyone",
        "company-wide",
        "across the company",
        "multiple departments",
        "entire sales team",
    ]

    access_or_outage = [
        "can't access",
        "cannot access",
        "can't log in",
        "cannot log in",
        "unable to sign in",
        "system down",
        "system is down",
        "production down",
        "outage",
        "locked out",
    ]

    if any(signal in text for signal in security_signals):
        return (
            "Critical",
            "The ticket mentions a potential security or privacy incident.",
        )

    has_widespread_impact = any(
        phrase in text for phrase in widespread_impact
    )
    has_access_or_outage = any(
        phrase in text for phrase in access_or_outage
    )

    if has_widespread_impact and has_access_or_outage:
        return (
            "Critical",
            "The ticket describes a potential team-wide access failure "
            "or service disruption.",
        )

    urgent_signals = [
        "urgent",
        "asap",
        "immediately",
        "right away",
        "in 30 minutes",
        "within 30 minutes",
        "major client meeting",
        "deadline",
        "locked out",
        "can't access",
        "cannot access",
        "can't log in",
        "cannot log in",
        "unable to sign in",
        "system down",
        "system is down",
        "outage",
    ]

    if any(signal in text for signal in urgent_signals):
        return (
            "High",
            "The ticket mentions an urgent timeline or an access/service issue.",
        )

    if category == "Feature Request":
        return (
            "Low",
            "The ticket appears to request a product improvement rather "
            "than report a current service disruption.",
        )

    if category == "General Inquiry":
        return (
            "Low",
            "The ticket does not contain predefined signals of urgency "
            "or major business impact.",
        )

    return (
        "Medium",
        "The ticket describes a support issue without a detected "
        "critical or urgent signal.",
    )


def assign_team(category, priority):
    """Recommend a team to review the ticket."""
    if category == "Security & Privacy":
        return "Security / Incident Response"

    if priority == "Critical":
        return "Support Incident Response"

    team_map = {
        "Billing & Payments": "Billing Support",
        "Account Access": "Account Support",
        "Technical Issue": "Technical Support",
        "Feature Request": "Product Team",
        "General Inquiry": "Customer Support",
    }

    return team_map.get(category, "Customer Support")


def recommend_next_steps(category, priority):
    """Return suggested actions for the support representative."""
    if priority == "Critical":
        return [
            "Follow the organization's urgent escalation or incident-response process.",
            "Confirm the number of affected users and the business impact.",
            "Follow approved security and privacy procedures; never request passwords.",
        ]

    steps_by_category = {
        "Security & Privacy": [
            "Follow the organization's security incident reporting process.",
            "Preserve relevant details according to internal policy.",
            "Do not request passwords, authentication codes, or sensitive records.",
        ],
        "Billing & Payments": [
            "Review the relevant invoice, payment, or subscription details.",
            "Verify the account using approved procedures.",
            "Explain the available resolution options and applicable policies.",
        ],
        "Account Access": [
            "Confirm which account or users are affected.",
            "Ask for the exact error message, without requesting credentials.",
            "Use the approved identity-verification and account-recovery process.",
        ],
        "Technical Issue": [
            "Ask for the steps that reproduce the issue and any error message.",
            "Check whether the issue affects one user or multiple users.",
            "Follow the troubleshooting and escalation process for the affected system.",
        ],
        "Feature Request": [
            "Clarify the customer problem the requested feature would solve.",
            "Ask how the customer handles the workflow today.",
            "Record the request for product review without promising delivery.",
        ],
        "General Inquiry": [
            "Clarify the customer's question and desired outcome.",
            "Identify the relevant documentation or support resource.",
            "Follow up with verified information.",
        ],
    }

    return steps_by_category.get(
        category,
        steps_by_category["General Inquiry"],
    )


def create_response_draft(category, priority):
    """Create an editable, generic support response draft."""
    issue_descriptions = {
        "Security & Privacy": "a potential security or privacy concern",
        "Billing & Payments": "a billing or payment concern",
        "Account Access": "an account access issue",
        "Technical Issue": "a technical issue",
        "Feature Request": "your product improvement suggestion",
        "General Inquiry": "your question",
    }

    priority_messages = {
        "Critical": (
            "Your description suggests there may be a significant "
            "business impact, so the issue should be reviewed promptly."
        ),
        "High": (
            "We understand that timing is important and will need to "
            "review the details of the issue."
        ),
        "Medium": (
            "We'll review the details to better understand the issue "
            "and determine appropriate next steps."
        ),
        "Low": (
            "We appreciate you sharing this with us and will review "
            "the details."
        ),
    }

    issue = issue_descriptions.get(
        category,
        "your support request",
    )
    priority_message = priority_messages.get(
        priority,
        priority_messages["Medium"],
    )

    return (
        "Hi there,\n\n"
        "Thanks for contacting support. I'm sorry you're experiencing "
        f"{issue}.\n\n"
        f"{priority_message} To help us investigate, please share "
        "any relevant error message and the steps that led to the issue. "
        "Please do not send passwords, authentication codes, or sensitive "
        "customer records.\n\n"
        "Best,\n"
        "Support Team"
    )


def analyze_ticket(ticket_text):
    """Analyze a ticket and return all recommendations."""
    if not ticket_text or not ticket_text.strip():
        raise ValueError("Please enter a customer support ticket.")

    category = categorize_ticket(ticket_text)
    priority, priority_reason = prioritize_ticket(
        ticket_text,
        category,
    )

    return {
        "category": category,
        "priority": priority,
        "priority_reason": priority_reason,
        "assigned_team": assign_team(category, priority),
        "next_steps": recommend_next_steps(category, priority),
        "draft_response": create_response_draft(category, priority),
    }
