
# Customer Support Ticket Triage Assistant

A Python and Streamlit application that helps support teams categorize customer tickets, identify potential urgency, recommend a support destination, and draft customer responses.

## Project Overview

Support teams often need to quickly understand incoming customer requests, identify business impact, and determine appropriate next steps.

This project demonstrates how a lightweight application can organize that workflow using transparent, predefined rules.

The current version is a working rule-based prototype. It does not connect to a live AI model or automatically create tickets, notify support teams, or contact customers.

## Live Demo

[Launch the Customer Support Ticket Triage Assistant](https://support-ticket-triage-assistant-ap6jzzahpvxqcydepzmkc3.streamlit.app/)

## Features

- **Ticket categorization:** Classifies issues into Security & Privacy, Billing & Payments, Account Access, Technical Issue, Feature Request, and General Inquiry.
- **Priority recommendations:** Suggests Critical, High, Medium, or Low priority based on predefined keywords and business-impact signals.
- **Team recommendations:** Suggests a support destination based on the detected category and priority.
- **Recommended next steps:** Provides guidance for the support representative.
- **Response drafting:** Generates an editable customer response.
- **Persistent editing:** Preserves the analysis and edited response when Streamlit reruns the application.
- **Human review guidance:** Reminds users to verify recommendations before taking action.

## Technology Stack

- Python
- Streamlit
- pytest
- GitHub
- GitHub Actions
- Streamlit Community Cloud

## How It Works

1. A representative enters a customer support ticket.
2. The application checks the text against predefined keyword rules.
3. The application assigns a category and recommends a priority.
4. A support destination and suggested next steps are displayed.
5. An editable customer response is generated.
6. The representative reviews the analysis and edits the response as needed.

The rules are intentionally transparent, but they can miss context or produce incorrect classifications. Priority recommendations require human review.

## Run Locally

### Prerequisites

- Python 3
- pip

### Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the application dependency:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Automated Testing

The project includes 21 automated tests covering ticket categorization, priority recommendations, support routing, response drafting, input validation, and Streamlit interface behavior.

Install pytest:

```bash
python -m pip install pytest
```

Run the test suite:

```bash
python -m pytest -q
```

The expected result is 21 passing tests.

## Responsible Use and Limitations

- The application uses keyword-based rules, not a live AI model.
- A recommended priority is not a guarantee of actual severity.
- Security and privacy concerns should follow the organization's incident-response process.
- Never request passwords, authentication codes, or sensitive customer records in a support response.
- Review ticket classifications, recommended actions, and response drafts before acting on them.
- Use fictional or anonymized customer information when testing.

## Future Improvements

- Expand test coverage for ambiguous and conflicting ticket signals.
- Improve prioritization using configurable business-impact rules.
- Add ticket history and structured reporting.
- Explore integrations with support platforms.
- Evaluate language-model integration through a securely configured API.
- Expand automated test coverage and CI checks.

## Project Goals

This project demonstrates practical skills in Python development, rule-based classification, support workflow design, application state management, automated testing, and user-interface development.
