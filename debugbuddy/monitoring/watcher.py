import time
import ast
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console

from debugbuddy.core.parser import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer

console = Console()

class ErrorWatcher:

    def __init__(self, directory, language='python', exclude=None):
        path = Path(directory).resolve()

        if path.is_file():
            self.directory = path.parent.resolve()
            self.target_file = path.resolve()
        elif path.suffix and path.parent.exists():
            self.directory = path.parent.resolve()
            self.target_file = path.resolve()
        else:
            if not path.exists():
                raise FileNotFoundError(f"Directory not found: {directory}")
            self.directory = path.resolve()
            self.target_file = None

        if not self.directory.exists():
            raise FileNotFoundError(f"Directory not found: {self.directory}")

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
            self.exclude,
            self.target_file
        )

        self.observer.schedule(
            event_handler,
            str(self.directory),
            recursive=True
        )

        self.observer.start()

        time.sleep(0.2)

        if self.target_file:
            target_path = self.target_file.resolve()
            if target_path.exists():
                event_handler._check_for_errors(target_path)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

class ErrorFileHandler(FileSystemEventHandler):

    def __init__(self, parser, explainer, extensions, exclude, target_file=None):
        self.parser = parser
        self.explainer = explainer
        self.extensions = extensions
        self.exclude = exclude
        self.target_file = target_file
        self.last_check = {}

    def on_modified(self, event):
        self._handle_file_event(event)

    def on_created(self, event):
        self._handle_file_event(event)

    def _handle_file_event(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path).resolve()

        if self.target_file:
            target_path = self.target_file.resolve() if isinstance(self.target_file, Path) else Path(self.target_file).resolve()
            if file_path != target_path:
                return

        if any(pattern in str(file_path) for pattern in self.exclude):
            return

        if file_path.suffix not in self.extensions:
            return

        now = time.time()
        file_key = str(file_path)
        if file_key in self.last_check:
            if now - self.last_check[file_key] < 1.5:
                return

        self.last_check[file_key] = now

        time.sleep(0.1)

        self._check_for_errors(file_path)

    def _check_for_errors(self, file_path):
        try:
            if not file_path.exists():
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if file_path.suffix == '.py':
                filename = str(file_path)
                lines = content.splitlines(keepends=True)
                current_lines = lines[:]
                all_errors = []
                max_iterations = 20

                for iteration in range(max_iterations):
                    current_content = ''.join(current_lines)
                    try:
                        ast.parse(current_content, filename=filename)
                        break
                    except (SyntaxError, IndentationError) as e:
                        error_type = type(e).__name__
                        lineno = e.lineno
                        msg = e.msg
                        error_msg = f"{error_type}: {msg}\n  File \"{filename}\", line {lineno}"
                        if hasattr(e, 'text') and e.text:
                            error_msg += f"\n    {e.text.rstrip()}\n    {' ' * (getattr(e, 'offset', 0) - 1) if getattr(e, 'offset', 0) else ''}^"
                        all_errors.append(error_msg)

                        if 0 <= lineno - 1 < len(current_lines):
                            offending_line = current_lines[lineno - 1]
                            stripped = offending_line.lstrip()
                            if stripped:
                                indent = offending_line[:-len(stripped)]
                                commented = indent + '#' + stripped
                                current_lines[lineno - 1] = commented

                else:
                    all_errors.append("Too many syntax errors to recover from automatically")

                current_content = ''.join(current_lines)

                seen = set()
                unique_errors = []
                for error in all_errors:
                    error_key = error.split('\n')[0].strip()
                    if error_key not in seen:
                        seen.add(error_key)
                        unique_errors.append(error)

                if unique_errors:
                    self._report_all_errors(file_path, unique_errors)

        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except Exception as e:
            console.print(f"[yellow]Warning: Could not check {file_path.name}: {e}[/yellow]")

    def _report_all_errors(self, file_path, all_errors):
        timestamp = time.strftime("%H:%M:%S")

        console.print(f"\n[{timestamp}] 🐛 Found {len(all_errors)} error(s) in {file_path.name}")

        for i, error_text in enumerate(all_errors, 1):
            parsed = self.parser.parse(error_text)
            if parsed:
                explanation = self.explainer.explain(parsed)
                error_type = parsed.get('type', 'Unknown Error')
                line_info = ""
                if parsed.get('line'):
                    line_info = f" (line {parsed['line']})"
                console.print(f"           [{i}] [red]{error_type}[/red]{line_info}")
                console.print(f"                [dim]{explanation['simple'][:70]}...[/dim]")
            else:
                first_line = error_text.split('\n')[0] if error_text else "Unknown error"
                console.print(f"           [{i}] [red]{first_line[:60]}...[/red]")

    def _report_error(self, file_path, error_text):
        timestamp = time.strftime("%H:%M:%S")

        console.print(f"\n[{timestamp}] 🐛 Error detected in {file_path.name}")

        parsed = self.parser.parse(error_text)
        if parsed:
            explanation = self.explainer.explain(parsed)
            console.print(f"           [red]{parsed['type']}[/red]")
            console.print(f"           [dim]{explanation['simple'][:80]}...[/dim]")
        else:
            first_line = error_text.split('\n')[0] if error_text else "Unknown error"
            console.print(f"           [red]{first_line[:60]}...[/red]")