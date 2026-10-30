
import pytest

from triage import (
    analyze_ticket,
    assign_team,
    categorize_ticket,
    create_response_draft,
    prioritize_ticket,
    recommend_next_steps,
)


def test_categorizes_account_access():
    category = categorize_ticket(
        "I am locked out of my account and cannot log in."
    )

    assert category == "Account Access"


def test_categorizes_billing_issue():
    category = categorize_ticket(
        "I was charged twice for my monthly subscription."
    )

    assert category == "Billing & Payments"


def test_categorizes_technical_issue():
    category = categorize_ticket(
        "The dashboard keeps crashing when I open reports."
    )

    assert category == "Technical Issue"


def test_categorizes_feature_request():
    category = categorize_ticket(
        "Could you add dark mode to the application?"
    )

    assert category == "Feature Request"


def test_categorizes_security_issue():
    category = categorize_ticket(
        "I noticed a suspicious login on my account."
    )

    assert category == "Security & Privacy"


def test_unknown_issue_uses_general_category():
    category = categorize_ticket(
        "What are your customer support hours?"
    )

    assert category == "General Inquiry"


def test_team_wide_access_failure_is_critical():
    ticket = (
        "Our entire sales team can't access customer records. "
        "We have an important client meeting in 30 minutes."
    )

    category = categorize_ticket(ticket)
    priority, reason = prioritize_ticket(ticket, category)

    assert category == "Account Access"
    assert priority == "Critical"
    assert reason


def test_security_issue_is_critical():
    ticket = "We discovered a possible data breach."
    category = categorize_ticket(ticket)
    priority, reason = prioritize_ticket(ticket, category)

    assert category == "Security & Privacy"
    assert priority == "Critical"
    assert "security" in reason.lower() or "privacy" in reason.lower()


def test_urgent_individual_access_issue_is_high():
    ticket = "I am locked out of my account and need access ASAP."

    category = categorize_ticket(ticket)
    priority, reason = prioritize_ticket(ticket, category)

    assert category == "Account Access"
    assert priority == "High"
    assert reason


def test_ordinary_billing_issue_is_medium():
    ticket = "I have a question about a charge on my invoice."

    category = categorize_ticket(ticket)
    priority, reason = prioritize_ticket(ticket, category)

    assert category == "Billing & Payments"
    assert priority == "Medium"
    assert reason


def test_feature_request_is_low_priority():
    ticket = "Could you add dark mode to the application?"

    category = categorize_ticket(ticket)
    priority, reason = prioritize_ticket(ticket, category)

    assert category == "Feature Request"
    assert priority == "Low"
    assert reason


def test_critical_ticket_has_incident_response_team():
    team = assign_team("Account Access", "Critical")

    assert team == "Support Incident Response"


def test_security_issue_routes_to_security_team():
    team = assign_team("Security & Privacy", "Critical")

    assert team == "Security / Incident Response"


def test_empty_ticket_is_rejected():
    with pytest.raises(ValueError, match="customer support ticket"):
        analyze_ticket("")

    with pytest.raises(ValueError, match="customer support ticket"):
        analyze_ticket("   ")


def test_analysis_returns_expected_fields():
    result = analyze_ticket(
        "I was charged twice for my subscription."
    )

    assert result["category"] == "Billing & Payments"
    assert result["priority"] == "Medium"
    assert result["assigned_team"] == "Billing Support"
    assert len(result["next_steps"]) > 0
    assert "draft_response" in result
    assert result["draft_response"].startswith("Hi there")


def test_response_draft_warns_against_sharing_credentials():
    draft = create_response_draft(
        "Account Access",
        "High",
    )

    assert "passwords" in draft.lower()
    assert "authentication codes" in draft.lower()


def test_security_ticket_includes_security_guidance():
    steps = recommend_next_steps(
        "Security & Privacy",
        "High",
    )

    assert any(
        "security incident" in step.lower()
        for step in steps
    )
