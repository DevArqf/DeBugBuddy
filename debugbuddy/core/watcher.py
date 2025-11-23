import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console

from debugbuddy.core.parser import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer

console = Console()

class ErrorWatcher:

    def __init__(self, directory, language='python', exclude=None):
        self.directory = Path(directory)
        self.language = language
        self.exclude = exclude or []
        self.parser = ErrorParser()
        self.explainer = ErrorExplainer()
        self.observer = Observer()

        self.extensions = {
            'python': ['.py'],
            'javascript': ['.js', '.jsx', '.ts', '.tsx'],
        }

    def start(self):

        event_handler = ErrorFileHandler(
            self.parser,
            self.explainer,
            self.extensions.get(self.language, ['.py']),
            self.exclude
        )

        self.observer.schedule(
            event_handler,
            str(self.directory),
            recursive=True
        )

        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

class ErrorFileHandler(FileSystemEventHandler):

    def __init__(self, parser, explainer, extensions, exclude):
        self.parser = parser
        self.explainer = explainer
        self.extensions = extensions
        self.exclude = exclude
        self.last_check = {}

    def on_modified(self, event):

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if any(pattern in str(file_path) for pattern in self.exclude):
            return

        if file_path.suffix not in self.extensions:
            return

        now = time.time()
        if file_path in self.last_check:
            if now - self.last_check[file_path] < 2:
                return

        self.last_check[file_path] = now

        self._check_for_errors(file_path)

    def _check_for_errors(self, file_path):

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if file_path.suffix == '.py':
                try:
                    compile(content, str(file_path), 'exec')
                except SyntaxError as e:
                    self._report_error(file_path, str(e))

        except Exception as e:
            pass

    def _report_error(self, file_path, error_text):

        timestamp = time.strftime("%H:%M:%S")

        console.print(f"\n[{timestamp}] 🐛 Error detected in {file_path.name}")

        parsed = self.parser.parse(error_text)
        if parsed:
            explanation = self.explainer.explain(parsed)
            console.print(f"           [red]{parsed['type']}[/red]")
            console.print(f"           [dim]{explanation['simple'][:80]}...[/dim]")