from pathlib import Path
from typing import Dict, List, Optional

from .app import ResultApp


def run_explain_view(parsed: Dict, explanation: Dict, similar: Optional[Dict]):
    title = "DeBugBuddy Explain"
    subtitle = parsed.get("type", "Unknown Error")

    body_lines = [
        "# Error",
        explanation.get("simple", "No explanation available."),
        "",
        "# Fix",
        explanation.get("fix", "No fix available."),
    ]

    example = explanation.get("example") or ""
    if example:
        body_lines.extend(["", "# Example", "```", example, "```"])

    did_you_mean = explanation.get("did_you_mean") or []
    if did_you_mean:
        body_lines.append("")
        body_lines.append("# Did you mean")
        body_lines.extend([f"- {item}" for item in did_you_mean])

    suggestions = explanation.get("suggestions") or []
    if suggestions:
        body_lines.append("")
        body_lines.append("# Suggestions")
        body_lines.extend([f"- {item}" for item in suggestions])

    if explanation.get("ai"):
        body_lines.extend(["", "# AI Explanation", explanation.get("ai")])

    sidebar_lines = [
        "## Details",
        f"- Type: {parsed.get('type', 'Unknown')}",
        f"- Language: {parsed.get('language', 'unknown')}",
    ]

    file_path = parsed.get("file")
    line = parsed.get("line")
    if file_path:
        sidebar_lines.append(f"- File: {file_path}")
    if line:
        sidebar_lines.append(f"- Line: {line}")

    if similar:
        sidebar_lines.extend(
            [
                "",
                "## Similar",
                f"- {similar.get('timestamp', '')}: {similar.get('error_type', '')}",
                f"- {similar.get('simple', '')}",
            ]
        )

    app = ResultApp(
        title=title,
        subtitle=subtitle,
        body="\n".join(body_lines),
        sidebar="\n".join(sidebar_lines),
    )
    app.run()


def run_history_stats_view(stats_data: Dict):
    title = "DeBugBuddy History"
    subtitle = "Error analytics"
    body = f"Total errors: {stats_data.get('total', 0)}"

    tables = []
    by_type = stats_data.get("by_type", {})
    if by_type:
        tables.append(
            {
                "title": "By Type",
                "columns": ["Type", "Count"],
                "rows": sorted(by_type.items(), key=lambda x: x[1], reverse=True),
            }
        )

    by_language = stats_data.get("by_language", {})
    if by_language:
        tables.append(
            {
                "title": "By Language",
                "columns": ["Language", "Count"],
                "rows": sorted(by_language.items(), key=lambda x: x[1], reverse=True),
            }
        )

    by_file = stats_data.get("by_file", {})
    if by_file:
        tables.append(
            {
                "title": "Top Files",
                "columns": ["File", "Count"],
                "rows": list(by_file.items()),
            }
        )

    recent_days = stats_data.get("recent_days", [])
    if recent_days:
        tables.append(
            {
                "title": "Last 7 Days",
                "columns": ["Day", "Count"],
                "rows": recent_days,
            }
        )

    app = ResultApp(title=title, subtitle=subtitle, body=body, tables=tables)
    app.run()


def run_history_entries_view(entries: List[Dict], title: str):
    rows = []
    for entry in entries:
        rows.append(
            [
                entry.get("timestamp", ""),
                entry.get("error_type", ""),
                entry.get("message", ""),
                entry.get("file") or "",
                entry.get("line") or "",
            ]
        )

    app = ResultApp(
        title="DeBugBuddy History",
        subtitle=title,
        tables=[
            {
                "title": "Entries",
                "columns": ["Timestamp", "Type", "Message", "File", "Line"],
                "rows": rows,
            }
        ],
    )
    app.run()


def run_predict_view(predictions: List[object]):
    rows = []
    for pred in predictions:
        rows.append(
            [
                Path(pred.file).name if pred.file else "",
                pred.line or "",
                pred.error_type,
                f"{pred.confidence * 100:.0f}%",
                pred.severity,
                pred.suggestion,
            ]
        )

    app = ResultApp(
        title="DeBugBuddy Predict",
        subtitle="Potential issues",
        tables=[
            {
                "title": "Predictions",
                "columns": ["File", "Line", "Type", "Confidence", "Severity", "Suggestion"],
                "rows": rows,
            }
        ],
    )
    app.run()


def run_search_view(results: List[Dict]):
    rows = []
    for pattern in results:
        rows.append(
            [
                pattern.get("name", ""),
                pattern.get("language", ""),
                pattern.get("description", ""),
            ]
        )

    app = ResultApp(
        title="DeBugBuddy Search",
        subtitle="Pattern results",
        tables=[
            {
                "title": "Patterns",
                "columns": ["Name", "Language", "Description"],
                "rows": rows,
            }
        ],
    )
    app.run()


def run_config_view(config: Dict):
    rows = [[k, str(v)] for k, v in config.items()]
    app = ResultApp(
        title="DeBugBuddy Config",
        subtitle="Current configuration",
        tables=[
            {
                "title": "Settings",
                "columns": ["Key", "Value"],
                "rows": rows,
            }
        ],
    )
    app.run()


def run_github_search_view(solutions: List[Dict]):
    rows = []
    for sol in solutions:
        rows.append(
            [
                sol.get("title", ""),
                sol.get("state", ""),
                sol.get("reactions", 0),
                sol.get("comments", 0),
                sol.get("url", ""),
            ]
        )

    app = ResultApp(
        title="DeBugBuddy GitHub",
        subtitle="Search results",
        tables=[
            {
                "title": "Solutions",
                "columns": ["Title", "State", "Reactions", "Comments", "URL"],
                "rows": rows,
            }
        ],
    )
    app.run()


def run_github_report_view(issue: Dict):
    body = "\n".join(
        [
            "# Issue Created",
            f"Title: {issue.get('title', '')}",
            "",
            f"URL: {issue.get('html_url', '')}",
        ]
    )
    app = ResultApp(title="DeBugBuddy GitHub", subtitle="Report issue", body=body)
    app.run()


def run_train_view(patterns: List[object]):
    rows = []
    for pattern in patterns:
        rows.append(
            [
                pattern.type,
                pattern.language,
                ", ".join(pattern.keywords),
            ]
        )

    app = ResultApp(
        title="DeBugBuddy Train",
        subtitle="Custom patterns",
        tables=[
            {
                "title": "Custom Patterns",
                "columns": ["Type", "Language", "Keywords"],
                "rows": rows,
            }
        ],
    )
    app.run()
