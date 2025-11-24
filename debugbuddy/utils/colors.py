from typing import Dict

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

def color_text(text: str, color: str) -> str:
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def print_colored(text: str, color: str):
    print(color_text(text, color))

def format_table_row(items: list, colors: list):
    colored_items = [color_text(item, colors[i % len(colors)]) for i, item in enumerate(items)]
    return ' | '.join(colored_items)