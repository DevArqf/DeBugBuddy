from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Utilities for formatting output, extract from current if any
class Formatter:
    @staticmethod
    def format_explanation(title, content):
        return Panel(content, title=title)
    # Add more