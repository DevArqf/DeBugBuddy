import os
import sys


def tui_available() -> bool:
    try:
        import textual  # noqa: F401
    except Exception:
        return False
    return True


def should_use_tui() -> bool:
    flag = os.environ.get("DEBUGBUDDY_TUI", "1").lower()
    if flag in {"0", "false", "no"}:
        return False
    if not sys.stdout.isatty():
        return False
    return tui_available()
