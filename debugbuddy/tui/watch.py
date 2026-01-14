import threading

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, RichLog, Static

from ..monitoring.watcher import ErrorWatcher


class WatchApp(App):
    CSS = """
    Screen {
        background: #0b0f14;
        color: #e6eef8;
    }
    #banner {
        padding: 1 2;
        color: #8ee3ff;
        text-style: bold;
    }
    RichLog {
        background: #0f1520;
        border: solid #1b2635;
        margin: 0 2 1 2;
    }
    """

    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.stop_event = threading.Event()
        self._thread = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(f"Watching: {self.path} (Ctrl+C to stop)", id="banner")
        yield RichLog(id="log", wrap=True)
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#log", RichLog)

        def emit(message: str):
            self.call_from_thread(log.write, message)

        watcher = ErrorWatcher(self.path, emit=emit, stop_event=self.stop_event)
        self._thread = threading.Thread(target=watcher.start, daemon=True)
        self._thread.start()

    def on_unmount(self) -> None:
        self.stop_event.set()


def run_watch_view(path: str):
    WatchApp(path).run()
