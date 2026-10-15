"""Lightweight issue classification and transparent priority heuristics."""

import re

CANDIDATE_LABELS = [
    "bug or software defect",
    "feature request or product enhancement",
    "documentation or installation problem",
    "performance or scalability problem",
    "security vulnerability or privacy concern",
    "user interface or accessibility problem",
    "question or usage support request",
    "build, deployment, or configuration problem",
    "testing or test coverage problem",
]

LABEL_TO_SLUG = {
    "bug or software defect": "bug",
    "feature request or product enhancement": "feature-request",
    "documentation or installation problem": "documentation",
    "performance or scalability problem": "performance",
    "security vulnerability or privacy concern": "security",
    "user interface or accessibility problem": "ui-accessibility",
    "question or usage support request": "question",
    "build, deployment, or configuration problem": "build-deployment",
    "testing or test coverage problem": "testing",
}

CATEGORY_KEYWORDS = {
    "bug or software defect": [
        "bug", "defect", "crash", "crashes", "crashing", "error", "exception",
        "broken", "fails", "failure", "not working", "incorrect",
    ],
    "feature request or product enhancement": [
        "feature", "add", "support", "enhancement", "implement", "dark mode",
        "request", "new option",
    ],
    "documentation or installation problem": [
        "documentation", "docs", "readme", "guide", "installation",
        "setup instructions", "tutorial",
    ],
    "performance or scalability problem": [
        "slow", "performance", "latency", "timeout", "scalability",
        "memory usage", "takes too long",
    ],
    "security vulnerability or privacy concern": [
        "security", "vulnerability", "exploit", "credential", "password",
        "data breach", "injection", "exposed",
    ],
    "user interface or accessibility problem": [
        "ui", "interface", "accessibility", "screen reader", "contrast",
        "button", "layout", "keyboard navigation",
    ],
    "question or usage support request": [
        "question", "how do i", "how to", "help", "usage", "clarification",
    ],
    "build, deployment, or configuration problem": [
        "build", "deploy", "deployment", "configuration", "config",
        "environment variable", "compile",
    ],
    "testing or test coverage problem": [
        "test", "tests", "test coverage", "coverage", "flaky", "unit test",
        "integration test",
    ],
}


def build_issue_text(title: str, body: str) -> str:
    """Combine an issue title and description into one input string."""
    title = (title or "").strip()
    body = (body or "").strip()
    if title and body:
        return f"Issue title: {title}\nIssue description: {body}"
    return title or body


def triage_issue(issue_text: str) -> dict:
    """Rank issue categories by local keyword matches without downloading a model."""
    text = (issue_text or "").lower()
    counts = {}
    for label in CANDIDATE_LABELS:
        counts[label] = sum(
            len(re.findall(r"\b" + re.escape(keyword) + r"\b", text))
            for keyword in CATEGORY_KEYWORDS[label]
        )

    if not any(counts.values()):
        counts["question or usage support request"] = 1

    ranked = sorted(
        enumerate(CANDIDATE_LABELS),
        key=lambda item: (-counts[item[1]], item[0]),
    )
    total_matches = sum(counts.values())
    return {
        "labels": [LABEL_TO_SLUG[label] for _, label in ranked],
        "scores": [counts[label] / total_matches for _, label in ranked],
    }


def recommend_priority(issue_text: str) -> tuple[str, str]:
    """
    Transparent rule-based priority suggestion.
    This is deliberately separate from category matching and must be reviewed by a human.
    """
    text = (issue_text or "").lower()

    critical_terms = [
        "data breach", "credentials exposed", "password in plain text",
        "remote code execution", "rce", "production down", "all users affected",
        "data loss", "delete all data",
    ]
    high_terms = [
        "security", "vulnerability", "crash", "crashes", "crashing",
        "cannot log in", "can't log in", "payment failed", "blocks release",
        "application down", "service unavailable",
    ]
    medium_terms = [
        "slow", "performance", "timeout", "fails", "failure",
        "not working", "error", "incorrect", "broken",
    ]

    if any(term in text for term in critical_terms):
        return "Critical", "A high-impact phrase was found (for example, exposed credentials, data loss, or production outage). Verify immediately."
    if any(term in text for term in high_terms):
        return "High", "The issue mentions a potential security concern, crash, access failure, or service disruption."
    if any(term in text for term in medium_terms):
        return "Medium", "The issue mentions an error, failure, slowness, or broken behavior."
    return "Low", "No configured high-impact keywords were found. This is only a default suggestion, not proof that the issue is low risk."
