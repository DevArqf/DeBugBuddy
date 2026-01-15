from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import (
    Button,
    ContentSwitcher,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    RichLog,
    Select,
    Static,
    Switch,
    TextArea,
)

from ..core.explainer import ErrorExplainer
from ..core.parsers import ErrorParser
from ..core.predictor import ErrorPredictor
from ..core.trainer import PatternTrainer
from ..integrations.github.client import GitHubClient
from ..integrations.github.search import GitHubSearcher
from ..models.training import TrainingData
from ..monitoring.watcher import ErrorWatcher
from ..storage.config import ConfigManager
from ..storage.history import HistoryManager


class DebugBuddyGUI(App):
    TITLE = "DeBugBuddy GUI"
    SUB_TITLE = "Terminal debugging companion"
    CSS = """
    Screen {
        background: #07100b;
        color: #e9f5ee;
    }
    #layout {
        height: 100%;
    }
    #sidebar {
        width: 28;
        background: #0b1710;
        border: none;
        padding: 1 1;
    }
    #content {
        background: #0a140f;
        border: none;
        padding: 1 2;
    }
    .section-title {
        color: #6ee7b7;
        text-style: bold;
        margin: 1 0 0 0;
    }
    .form-row {
        height: auto;
        margin: 1 0;
    }
    TextArea {
        height: 8;
    }
    Input, Select {
        width: 1fr;
        border: none;
        background: #0f1f16;
        color: #e9f5ee;
    }
    Select * {
        border: none;
    }
    Button {
        min-width: 10;
        border: none;
        background: #1f6b3a;
        color: #f1fff7;
    }
    #explain-actions {
        margin-left: 2;
    }
    #explain-actions > * {
        margin-right: 2;
    }
    #explain-row {
        height: auto;
        margin: 1 0;
    }
    #explain-lang {
        width: 36;
    }
    #explain-spacer {
        width: 1fr;
    }
    .button, .input, .select, .select--button, .select--dropdown, .switch {
        border: none;
    }
    Switch, Switch * {
        border: none;
    }
    DataTable {
        border: none;
        background: #0a140f;
    }
    ListView {
        background: #0b1710;
        border: none;
    }
    TextArea {
        border: none;
        background: #0f1f16;
    }
    ListItem.--highlight {
        background: #1f6b3a;
        color: #f1fff7;
    }
    ListItem {
    }
    RichLog {
        background: #0f1f16;
        color: #d9fbe7;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="layout"):
            with VerticalScroll(id="sidebar"):
                yield Label("DeBugBuddy GUI", id="brand")
                yield ListView(
                    ListItem(Label("Explain"), id="nav-explain"),
                    ListItem(Label("Predict"), id="nav-predict"),
                    ListItem(Label("History"), id="nav-history"),
                    ListItem(Label("Search"), id="nav-search"),
                    ListItem(Label("Config"), id="nav-config"),
                    ListItem(Label("GitHub"), id="nav-github"),
                    ListItem(Label("Watch"), id="nav-watch"),
                    ListItem(Label("Train"), id="nav-train"),
                    id="nav",
                )
            with Container(id="content"):
                yield ContentSwitcher(
                    ExplainView(id="view-explain"),
                    PredictView(id="view-predict"),
                    HistoryView(id="view-history"),
                    SearchView(id="view-search"),
                    ConfigView(id="view-config"),
                    GitHubView(id="view-github"),
                    WatchView(id="view-watch"),
                    TrainView(id="view-train"),
                    id="switcher",
                )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#nav", ListView).index = 0
        self._show_view("explain")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id or ""
        if item_id.startswith("nav-"):
            self._show_view(item_id.replace("nav-", ""))

    def _show_view(self, name: str) -> None:
        switcher = self.query_one("#switcher", ContentSwitcher)
        switcher.current = f"view-{name}"


class ExplainView(VerticalScroll):
    BINDINGS = [("ctrl+enter", "run_explain", "Run explain")]

    def compose(self) -> ComposeResult:
        yield Label("Explain an error", classes="section-title")
        yield TextArea(placeholder="Paste the error message here...", id="explain-input")
        with Horizontal(id="explain-row"):
            yield Select(
                [
                    ("Auto", Select.BLANK),
                    ("Python", "python"),
                    ("JavaScript", "javascript"),
                    ("TypeScript", "typescript"),
                    ("C/C++", "c"),
                    ("PHP", "php"),
                    ("Java", "java"),
                    ("Ruby", "ruby"),
                ],
                id="explain-lang",
                allow_blank=True,
            )
            yield Static("", id="explain-spacer")
            with Horizontal(id="explain-actions"):
                yield Label("AI")
                yield Switch(id="explain-ai")
                yield Button("Explain", id="explain-run", variant="primary")
        yield Label("Tip: Press Ctrl+Enter to run.", id="explain-tip")
        yield Markdown("", id="explain-output")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "explain-run":
            return
        self._run_explain()

    def action_run_explain(self) -> None:
        self._run_explain()

    def _run_explain(self) -> None:
        error_text = self.query_one("#explain-input", TextArea).text.strip()
        if not error_text:
            self.query_one("#explain-output", Markdown).update("Provide an error message.")
            return
        language = self.query_one("#explain-lang", Select).value or None
        use_ai = self.query_one("#explain-ai", Switch).value

        parser = ErrorParser()
        explainer = ErrorExplainer()
        history = HistoryManager()
        config_mgr = ConfigManager()

        parsed = parser.parse(error_text, language=language)
        explanation = explainer.explain(parsed)

        if use_ai:
            from ..integrations.ai import get_provider
            provider_name = config_mgr.get("ai_provider", "openai")
            api_key = config_mgr.get(f"{provider_name}_api_key")
            if api_key:
                provider = get_provider(provider_name, config_mgr.get_all())
                if provider:
                    ai_explain = provider.explain_error(error_text, parsed.get("language", "code"))
                    if ai_explain:
                        explanation["ai"] = ai_explain

        history.add(parsed, explanation)
        similar = history.find_similar(parsed)

        body_lines = [
            f"**Type:** {parsed.get('type', 'Unknown')}",
            f"**Language:** {parsed.get('language', 'unknown')}",
        ]
        if parsed.get("file"):
            body_lines.append(f"**File:** {parsed.get('file')}")
        if parsed.get("line"):
            body_lines.append(f"**Line:** {parsed.get('line')}")

        content = [
            "# Error",
            explanation.get("simple", "No explanation."),
            "",
            "# Fix",
            explanation.get("fix", "No fix."),
        ]

        if explanation.get("example"):
            content.extend(["", "# Example", "```", explanation["example"], "```"])

        if explanation.get("did_you_mean"):
            content.append("")
            content.append("# Did you mean")
            content.extend([f"- {item}" for item in explanation["did_you_mean"]])

        if explanation.get("ai"):
            content.extend(["", "# AI Explanation", explanation["ai"]])

        if similar:
            content.extend(
                [
                    "",
                    "# Similar",
                    f"{similar.get('timestamp', '')}: {similar.get('error_type', '')}",
                    similar.get("simple", ""),
                ]
            )

        output = "\n".join(body_lines + [""] + content)
        self.query_one("#explain-output", Markdown).update(output)


class PredictView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Predict potential errors", classes="section-title")
        yield Input(placeholder="File path", id="predict-path")
        with Horizontal(classes="form-row"):
            yield Select(
                [
                    ("All severities", Select.BLANK),
                    ("Low", "low"),
                    ("Medium", "medium"),
                    ("High", "high"),
                    ("Critical", "critical"),
                ],
                id="predict-severity",
                allow_blank=True,
            )
            yield Input(placeholder="Limit (default 10)", id="predict-limit")
            yield Button("Run", id="predict-run", variant="primary")
        yield DataTable(id="predict-table")
        yield Label("", id="predict-status")

    def on_mount(self) -> None:
        table = self.query_one("#predict-table", DataTable)
        table.add_columns("File", "Line", "Type", "Confidence", "Severity", "Suggestion")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "predict-run":
            return
        self._run_predict()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in {"predict-path", "predict-severity", "predict-limit"}:
            self._run_predict()

    def _run_predict(self) -> None:
        path_value = self.query_one("#predict-path", Input).value.strip()
        if not path_value:
            self.query_one("#predict-status", Label).update("Provide a file path.")
            return
        severity = self.query_one("#predict-severity", Select).value or None
        limit_value = self.query_one("#predict-limit", Input).value.strip()
        limit = int(limit_value) if limit_value.isdigit() else 10

        predictor = ErrorPredictor(ConfigManager())
        try:
            predictions = predictor.predict_file(Path(path_value))
        except Exception as exc:
            self.query_one("#predict-status", Label).update(f"Prediction failed: {exc}")
            return
        if severity:
            predictions = [p for p in predictions if p.severity == severity]
        predictions = predictions[:limit]

        table = self.query_one("#predict-table", DataTable)
        table.clear()
        if not predictions:
            self.query_one("#predict-status", Label).update("No potential errors detected.")
            return
        self.query_one("#predict-status", Label).update("")
        for pred in predictions:
            table.add_row(
                Path(pred.file).name if pred.file else "",
                str(pred.line or ""),
                pred.error_type,
                f"{pred.confidence * 100:.0f}%",
                pred.severity,
                pred.suggestion,
            )


class HistoryView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("History", classes="section-title")
        with Horizontal(classes="form-row"):
            yield Select(
                [
                    ("Recent", "recent"),
                    ("Stats", "stats"),
                ],
                id="history-mode",
            )
            yield Button("Run", id="history-run", variant="primary")
        with Horizontal(classes="form-row"):
            yield Input(placeholder="Search keyword", id="history-search")
            yield Button("Search", id="history-search-run", variant="primary")
        yield DataTable(id="history-table")

    def on_mount(self) -> None:
        table = self.query_one("#history-table", DataTable)
        table.add_columns("Timestamp", "Type", "Message", "File", "Line")

    def _set_rows(self, rows: List[List[str]]) -> None:
        table = self.query_one("#history-table", DataTable)
        table.clear()
        for row in rows:
            table.add_row(*row)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        history = HistoryManager()
        if event.button.id == "history-run":
            mode = self.query_one("#history-mode", Select).value or "recent"
            if mode == "stats":
                stats = history.get_stats()
                rows = []
                rows.append(["-- Types --", "", "", "", ""])
                for typ, count in sorted(stats.get("by_type", {}).items(), key=lambda x: x[1], reverse=True):
                    rows.append([f"type: {typ}", str(count), "", "", ""])
                rows.append(["-- Languages --", "", "", "", ""])
                for lang, count in sorted(stats.get("by_language", {}).items(), key=lambda x: x[1], reverse=True):
                    rows.append([f"lang: {lang}", str(count), "", "", ""])
                self._set_rows(rows)
                return
            entries = history.get_recent()
            rows = [
                [
                    entry.get("timestamp", ""),
                    entry.get("error_type", ""),
                    entry.get("message", ""),
                    entry.get("file") or "",
                    str(entry.get("line") or ""),
                ]
                for entry in entries
            ]
            self._set_rows(rows)
        elif event.button.id == "history-search-run":
            self._run_search(history)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "history-search":
            self._run_search(HistoryManager())

    def _run_search(self, history: HistoryManager) -> None:
        keyword = self.query_one("#history-search", Input).value.strip()
        if not keyword:
            return
        entries = history.search(keyword)
        rows = [
            [
                entry.get("timestamp", ""),
                entry.get("error_type", ""),
                entry.get("message", ""),
                entry.get("file") or "",
                str(entry.get("line") or ""),
            ]
            for entry in entries
        ]
        self._set_rows(rows)


class SearchView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Search patterns", classes="section-title")
        with Horizontal(classes="form-row"):
            yield Input(placeholder="Keyword", id="search-keyword")
            yield Button("Search", id="search-run", variant="primary")
        yield DataTable(id="search-table")

    def on_mount(self) -> None:
        table = self.query_one("#search-table", DataTable)
        table.add_columns("Name", "Language", "Description")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "search-run":
            return
        self._run_search()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search-keyword":
            self._run_search()

    def _run_search(self) -> None:
        keyword = self.query_one("#search-keyword", Input).value.strip()
        if not keyword:
            return
        results = ErrorExplainer().search_patterns(keyword)
        table = self.query_one("#search-table", DataTable)
        table.clear()
        for pattern in results:
            table.add_row(
                pattern.get("name", ""),
                pattern.get("language", ""),
                pattern.get("description", ""),
            )


class ConfigView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Configuration", classes="section-title")
        with Horizontal(classes="form-row"):
            yield Input(placeholder="Key", id="config-key")
            yield Input(placeholder="Value", id="config-value")
            yield Button("Set", id="config-set", variant="primary")
            yield Button("Refresh", id="config-refresh")
        yield DataTable(id="config-table")

    def on_mount(self) -> None:
        table = self.query_one("#config-table", DataTable)
        table.add_columns("Key", "Value")
        self._load_config()

    def _load_config(self):
        config = ConfigManager().get_all()
        table = self.query_one("#config-table", DataTable)
        table.clear()
        for key, value in config.items():
            table.add_row(key, str(value))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "config-set":
            self._set_config()
        elif event.button.id == "config-refresh":
            self._load_config()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in {"config-key", "config-value"}:
            self._set_config()

    def _set_config(self) -> None:
        key = self.query_one("#config-key", Input).value.strip()
        value = self.query_one("#config-value", Input).value.strip()
        if key:
            ConfigManager().set(key, value)
            self._load_config()


class GitHubView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("GitHub", classes="section-title")
        yield TextArea(placeholder="Error text", id="gh-error")
        with Horizontal(classes="form-row"):
            yield Select(
                [
                    ("Python", "python"),
                    ("JavaScript", "javascript"),
                    ("TypeScript", "typescript"),
                    ("C/C++", "c"),
                    ("PHP", "php"),
                    ("Java", "java"),
                    ("Ruby", "ruby"),
                ],
                id="gh-language",
                value="python",
            )
            yield Button("Search", id="gh-search", variant="primary")
        with Horizontal(classes="form-row"):
            yield Input(placeholder="Repo scope (owner/name)", id="gh-scope")
            yield Input(placeholder="Repo (owner/name)", id="gh-repo")
            yield Button("Report", id="gh-report")
        with Horizontal(classes="form-row"):
            yield Label("Exact")
            yield Switch(id="gh-exact", value=True)
            yield Label("Include closed")
            yield Switch(id="gh-closed")
        yield DataTable(id="gh-table")

    def on_mount(self) -> None:
        table = self.query_one("#gh-table", DataTable)
        table.add_columns("Title", "State", "Reactions", "Comments", "URL")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        error_text = self.query_one("#gh-error", TextArea).text.strip()
        config = ConfigManager()
        token = config.get("github_token")
        if event.button.id == "gh-search":
            self._run_search(error_text, token)
        elif event.button.id == "gh-report":
            self._run_report(error_text, token)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "gh-repo":
            error_text = self.query_one("#gh-error", TextArea).text.strip()
            config = ConfigManager()
            self._run_report(error_text, config.get("github_token"))
        elif event.input.id == "gh-scope":
            error_text = self.query_one("#gh-error", TextArea).text.strip()
            config = ConfigManager()
            self._run_search(error_text, config.get("github_token"))

    def _run_search(self, error_text: str, token: Optional[str]) -> None:
        if not error_text:
            return
        language = self.query_one("#gh-language", Select).value or "python"
        repo = self.query_one("#gh-scope", Input).value.strip() or None
        exact = self.query_one("#gh-exact", Switch).value
        include_closed = self.query_one("#gh-closed", Switch).value
        client = GitHubClient(token)
        searcher = GitHubSearcher(client)
        solutions = searcher.find_solutions(
            error_text,
            language,
            repo=repo,
            exact=exact,
            include_closed=include_closed,
        )
        table = self.query_one("#gh-table", DataTable)
        table.clear()
        for sol in solutions:
            table.add_row(
                sol.get("title", ""),
                sol.get("state", ""),
                str(sol.get("reactions", "")),
                str(sol.get("comments", "")),
                sol.get("url", ""),
            )

    def _run_report(self, error_text: str, token: Optional[str]) -> None:
        if not error_text:
            return
        repo = self.query_one("#gh-repo", Input).value.strip()
        if not repo:
            return
        client = GitHubClient(token)
        title = f"[DeBugBuddy] {error_text[:50]}"
        body = f"Error reported via DeBugBuddy:\n\n```\n{error_text}\n```"
        issue = client.create_issue(repo, title, body, labels=["bug", "debugbuddy"])
        table = self.query_one("#gh-table", DataTable)
        table.clear()
        table.add_row(issue.get("title", ""), "created", "", "", issue.get("html_url", ""))


class WatchView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Watch files", classes="section-title")
        with Horizontal(classes="form-row"):
            yield Input(placeholder="Path", id="watch-path")
            yield Button("Start", id="watch-start", variant="primary")
            yield Button("Stop", id="watch-stop")
        yield RichLog(id="watch-log", wrap=True)
        self._watcher = None
        self._watch_thread = None
        self._watch_stop = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "watch-start":
            self._run_watch_start()
        elif event.button.id == "watch-stop":
            if self._watch_stop:
                self._watch_stop.set()
            self._watcher = None
            self._watch_thread = None
            self._watch_stop = None

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "watch-path":
            self._run_watch_start()

    def _run_watch_start(self) -> None:
        path = self.query_one("#watch-path", Input).value.strip() or "."
        log = self.query_one("#watch-log", RichLog)
        if self._watch_thread:
            return
        import threading

        self._watch_stop = threading.Event()
        emit = lambda message: self.app.call_from_thread(log.write, message)
        self._watcher = ErrorWatcher(path, emit=emit, stop_event=self._watch_stop)
        self._watch_thread = threading.Thread(target=self._watcher.start, daemon=True)
        self._watch_thread.start()
        log.write(f"Watching: {path}")


class TrainView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Train patterns", classes="section-title")
        with Horizontal(classes="form-row"):
            yield Button("List Patterns", id="train-list", variant="primary")
            yield Button("Train From History", id="train-history")
            yield Button("Train ML", id="train-ml")
        yield DataTable(id="train-table")
        yield RichLog(id="train-log", wrap=True)

    def on_mount(self) -> None:
        table = self.query_one("#train-table", DataTable)
        table.add_columns("Type", "Language", "Keywords")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        trainer = PatternTrainer(ConfigManager())
        log = self.query_one("#train-log", RichLog)
        if event.button.id == "train-list":
            patterns = trainer.list_custom_patterns()
            table = self.query_one("#train-table", DataTable)
            table.clear()
            for pattern in patterns:
                table.add_row(pattern.type, pattern.language, ", ".join(pattern.keywords))
        elif event.button.id == "train-history":
            history = HistoryManager()
            recent = history.get_recent(limit=100)
            if not recent:
                log.write("No history entries found.")
                return
            error_groups: Dict[str, List[Dict]] = {}
            for entry in recent:
                error_groups.setdefault(entry["error_type"], []).append(entry)
            for error_type, entries in error_groups.items():
                if len(entries) < 3:
                    continue
                examples: List[TrainingData] = []
                for entry in entries[:5]:
                    examples.append(
                        TrainingData(
                            error_text=entry["message"],
                            explanation=entry["simple"],
                            fix=entry["fix"],
                            language=entry["language"],
                        )
                    )
                pattern = trainer.train_pattern(examples)
                log.write(f"Created pattern: {pattern.type}")
            log.write("Training from history complete.")
        elif event.button.id == "train-ml":
            try:
                from ..models.ml_engine import MLEngine, TrainingExample
                history = HistoryManager()
                recent = history.get_recent(limit=1000)
                if len(recent) < 10:
                    log.write(f"Not enough data (found {len(recent)}).")
                    return
                examples = [
                    TrainingExample(
                        error_text=entry["message"],
                        error_type=entry["error_type"],
                        language=entry["language"],
                    )
                    for entry in recent
                ]
                engine = MLEngine()
                engine.train_classifier(examples, epochs=20)
                engine.train_embeddings(examples, epochs=5)
                engine.save_models()
                ConfigManager().set("use_ml_prediction", True)
                log.write("ML training complete.")
            except Exception as exc:
                log.write(f"ML training failed: {exc}")


def run():
    DebugBuddyGUI().run()
