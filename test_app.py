
from streamlit.testing.v1 import AppTest


CRITICAL_TICKET = (
    "Our entire sales team can't access customer records. "
    "We've been blocked for three hours, and we have a major "
    "client meeting in 30 minutes. We need this fixed immediately."
)


def test_app_opens_without_errors():
    app = AppTest.from_file("app.py").run()

    assert not app.exception


def test_empty_ticket_shows_warning():
    app = AppTest.from_file("app.py").run()

    app.button[0].click().run()

    assert len(app.warning) > 0


def test_critical_ticket_displays_correct_assessment():
    app = AppTest.from_file("app.py").run()

    app.text_area[0].set_value(CRITICAL_TICKET)
    app.button[0].click().run()

    assert not app.exception

    result = app.session_state["ticket_result"]

    assert result["category"] == "Account Access"
    assert result["priority"] == "Critical"
    assert result["assigned_team"] == "Support Incident Response"
    assert len(result["next_steps"]) > 0


def test_response_edit_persists_and_results_remain_visible():
    app = AppTest.from_file("app.py").run()

    app.text_area[0].set_value(CRITICAL_TICKET)
    app.button[0].click().run()

    assert not app.exception
    assert len(app.text_area) >= 2

    original_result = app.session_state["ticket_result"]

    edited_response = (
        app.text_area[1].value
        + "\nI will follow up with you shortly."
    )

    app.text_area[1].set_value(edited_response).run()

    assert not app.exception
    assert (
        "I will follow up with you shortly."
        in app.text_area[1].value
    )
    assert (
        app.session_state["ticket_result"]["priority"]
        == original_result["priority"]
    )
    assert any(
        "1. Ticket assessment" in heading.value
        for heading in app.subheader
    )
