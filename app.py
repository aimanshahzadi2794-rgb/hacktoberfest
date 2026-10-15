import csv
import io
from datetime import datetime

import streamlit as st

from triage import (
    build_issue_text,
    recommend_priority,
    triage_issue,
)

st.set_page_config(
    page_title="IssuePilot AI",
    page_icon="🧭",
    layout="wide",
)

st.title("🧭 IssuePilot AI")
st.caption("Local, lightweight issue triage • No model download required")

with st.sidebar:
    st.header("About this MVP")
    st.write(
        "IssuePilot ranks likely issue categories using local keyword matching. "
        "Priority is a separate, transparent rule-based suggestion."
    )
    st.markdown("**Classifier**")
    st.write("Built-in keyword classifier; runs locally and needs no model download.")

examples = {
    "Bug: PDF upload crashes": {
        "title": "App crashes when uploading a PDF",
        "body": "When I upload a PDF larger than 5 MB, the page freezes and then the application crashes. This worked in the previous version.",
    },
    "Feature request: dark mode": {
        "title": "Add a dark mode option",
        "body": "It would be helpful to have a dark theme that users can enable from settings, especially when using the app at night.",
    },
    "Performance: slow dashboard": {
        "title": "Dashboard takes 20 seconds to load",
        "body": "The dashboard is very slow when there are many records. The page takes around 20 seconds to become usable.",
    },
    "Security: password exposed": {
        "title": "Password appears in application logs",
        "body": "I noticed that a user's password is written in plain text in the server logs. This could expose credentials to anyone with log access.",
    },
    "Documentation: missing setup steps": {
        "title": "Installation guide is missing steps",
        "body": "The README does not explain how to configure the environment variables, so new contributors cannot start the project.",
    },
}

st.subheader("1. Enter an issue")
example_choice = st.selectbox("Or load a demo example", ["— Choose an example —", *examples.keys()])

default_title = ""
default_body = ""
if example_choice in examples:
    default_title = examples[example_choice]["title"]
    default_body = examples[example_choice]["body"]

with st.form("issue_form"):
    title = st.text_input("Issue title", value=default_title, placeholder="e.g. App crashes when uploading a PDF")
    body = st.text_area(
        "Issue description",
        value=default_body,
        height=180,
        placeholder="Describe what happened, what you expected, and steps to reproduce...",
    )
    submitted = st.form_submit_button("🔍 Analyze issue", type="primary", use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []

if submitted:
    issue_text = build_issue_text(title, body)
    if len(issue_text.strip()) < 12:
        st.warning("Please enter a title or description with a little more detail.")
    else:
        with st.spinner("Analyzing issue..."):
            result = triage_issue(issue_text)
            priority, priority_reason = recommend_priority(issue_text)
            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": title.strip() or "(untitled issue)",
                "description": body.strip(),
                "category": result["labels"][0],
                "keyword_match_score": round(float(result["scores"][0]), 4),
                "priority": priority,
                "priority_reason": priority_reason,
                "top_labels": "; ".join(
                    f"{label} ({score:.1%})"
                    for label, score in zip(result["labels"][:3], result["scores"][:3])
                ),
            }
            st.session_state.latest = record
            st.session_state.history.insert(0, record)

if "latest" in st.session_state:
    record = st.session_state.latest
    st.divider()
    st.subheader("2. Triage result")

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted category", record["category"].replace("-", " ").title())
    col2.metric("Keyword match score", f"{record['keyword_match_score']:.1%}")
    col3.metric("Suggested priority", record["priority"])

    st.caption(
        "Category scores show each category's share of keyword matches. They are not probabilities "
        "or a measure of prediction accuracy."
    )

    st.markdown("**Top category matches**")
    result_rows = []
    for item in st.session_state.history:
        if item["timestamp"] == record["timestamp"] and item["title"] == record["title"]:
            result_rows = [
                {"Category": label, "Score": score}
                for label, score in zip(
                    st.session_state.get("latest_labels", []),
                    st.session_state.get("latest_scores", []),
                )
            ]
            break

    # Reconstruct the displayed top labels from the saved text so exports and UI remain simple.
    st.write(record["top_labels"])
    st.markdown("**Why this priority was suggested**")
    st.write(record["priority_reason"])
    st.markdown("**Issue reviewed**")
    st.write(record["title"])
    if record["description"]:
        st.write(record["description"])

st.divider()
st.subheader("3. Session history")
if st.session_state.history:
    st.dataframe(
        [
            {
                "Time": item["timestamp"],
                "Title": item["title"],
                "Category": item["category"],
                "Keyword match score": f"{item['keyword_match_score']:.1%}",
                "Priority": item["priority"],
            }
            for item in st.session_state.history
        ],
        use_container_width=True,
        hide_index=True,
    )
    output = io.StringIO()
    fieldnames = list(st.session_state.history[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(st.session_state.history)
    st.download_button(
        "⬇️ Download session history as CSV",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="issuepilot-triage-history.csv",
        mime="text/csv",
    )
    if st.button("Clear session history"):
        st.session_state.history = []
        st.session_state.pop("latest", None)
        st.rerun()
else:
    st.write("Your analyzed issues will appear here during this session.")

st.caption("MVP note: results are suggestions. A human should review security and high-priority issues.")
