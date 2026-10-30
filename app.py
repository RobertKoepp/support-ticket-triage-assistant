
import streamlit as st

from triage import analyze_ticket


st.set_page_config(
    page_title="Customer Support Ticket Triage",
    page_icon="🎫",
    layout="centered",
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 950px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1 {
            font-weight: 750;
            letter-spacing: -0.03em;
        }

        div.stButton > button {
            border-radius: 10px;
            min-height: 2.7rem;
            font-weight: 600;
        }

        [data-testid="stTextArea"] textarea {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "ticket_result" not in st.session_state:
    st.session_state.ticket_result = None

if "ticket_warning" not in st.session_state:
    st.session_state.ticket_warning = ""

if "response_draft" not in st.session_state:
    st.session_state.response_draft = ""

st.title("🎫 Customer Support Ticket Triage")
st.caption("Support operations prototype")

st.info(
    "Prototype mode: ticket categories and priority recommendations "
    "are generated using predefined Python rules, not a live AI model. "
    "Review the recommendations before acting on them."
)

with st.sidebar:
    st.header("About this tool")

    st.write(
        "This prototype helps support teams organize incoming tickets, "
        "identify potential urgency, and prepare response drafts."
    )

    st.divider()

    st.subheader("What it does")

    st.markdown(
        """
        - Categorizes customer issues
        - Recommends a priority
        - Suggests a support team
        - Lists possible next steps
        - Generates an editable response
        """
    )

    st.divider()

    st.subheader("Important limitations")

    st.write(
        "Keyword rules can misclassify tickets or miss important context. "
        "Critical issues must be reviewed by an authorized person."
    )

ticket_text = st.text_area(
    "Customer support ticket",
    height=190,
    placeholder=(
        "Example: Our entire sales team can't access customer records, "
        "and we have a major client meeting in 30 minutes."
    ),
    key="ticket_text",
)

if st.button("Analyze ticket", type="primary"):
    st.session_state.ticket_warning = ""

    if not ticket_text.strip():
        st.session_state.ticket_result = None
        st.session_state.response_draft = ""
        st.session_state.ticket_warning = (
            "Please enter a customer support ticket."
        )
    else:
        try:
            result = analyze_ticket(ticket_text)
            st.session_state.ticket_result = result
            st.session_state.response_draft = result["draft_response"]
        except ValueError as error:
            st.session_state.ticket_result = None
            st.session_state.response_draft = ""
            st.session_state.ticket_warning = str(error)

if st.session_state.ticket_warning:
    st.warning(st.session_state.ticket_warning)

if st.session_state.ticket_result is not None:
    result = st.session_state.ticket_result

    st.divider()
    st.subheader("1. Ticket assessment")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Category", result["category"])

    with col2:
        st.metric("Recommended priority", result["priority"])

    with col3:
        st.metric("Suggested team", result["assigned_team"])

    st.write("**Why this priority?**")
    st.write(result["priority_reason"])

    st.caption(
        "Priority is a rules-based recommendation, not an automatic "
        "escalation or a guarantee that the issue has been assigned."
    )

    st.subheader("2. Recommended next steps")

    for step in result["next_steps"]:
        st.markdown(f"- {step}")

    st.subheader("3. Suggested customer response")

    st.text_area(
        "Edit the response before using it",
        height=240,
        key="response_draft",
    )

    st.warning(
        "Human review required. Verify the diagnosis, urgency, policies, "
        "and response before taking action or contacting the customer."
    )

    st.success("Ticket analysis complete.")
