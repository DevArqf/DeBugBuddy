import sys
from .cli import main as cli_main
from .tui.runner import should_use_tui


def main():
    if len(sys.argv) == 1 and should_use_tui():
        from .tui.shell import run
        run()
        return
    cli_main()


if __name__ == "__main__":
    main()
