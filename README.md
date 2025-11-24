<div align="center">
<img width="1000" height="650" alt="DeBugBuddy Logo" src="https://github.com/DevArqf/DeBugBuddy/blob/main/DeBugBuddy%20Logo.png" />

### Your terminal’s debugging companion

Stop Googling. Understand your errors.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/pypi-v0.2.2-orange.svg)](https://pypi.org/project/debugbuddy-cli/0.2.2/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Install](#installation) •
[Quick Start](#quick-start) •
[Docs](#documentation)

</div>

---

## Installation

```bash
pip install debugbuddy-cli
```

## Quick Start

```bash
dbug explain "NameError: name 'x' is not defined"
dbug explain error.log
python script.py 2>&1 | dbug explain
dbug interactive
```

### Example Output

```bash
$ dbug explain "NameError: name 'user_id' is not defined"

╭─────────────────── 🐛 Error Explanation ───────────────────╮
│ NameError                                                  │
│ File: app.py, Line 42                                      │
│                                                            │
│ 🔍 You're trying to use 'user_id', but Python doesn't     │
│ know what that is yet.                                     │
│                                                            │
│ 💡 Did you mean?                                           │
│   • Check spelling of 'user_id'                            │
│   • Did you forget to define 'user_id'?                    │
│   • Need to import 'user_id'?                              │
│                                                            │
│ ✅ How to fix:                                             │
│   • Define it before using: user_id = 123                  │
│   • Import it: from config import user_id                  │
│   • Check for typos in the name                            │
╰────────────────────────────────────────────────────────────╯

💭 You've seen this type of error before
   Last occurrence: 2 hours ago

💡 Tip: Use dbug explain -e to see code examples
```

## Documentation

```bash
All Commands

dbug explain <error>
dbug interactive
dbug watch <dir>
dbug history
dbug history --stats
dbug search <keyword>
dbug config --show
dbug config --reset
dbug --version
```

```bash
Extra Options

dbug explain -e "SyntaxError: invalid syntax"
dbug explain -v error.log
dbug watch src/ --lang [CODING-LANG]
dbug config ai_provider openai
dbug config language [CODING-LANG]
dbug config languages "" (Disables language filtering)
dbug explain --ai "complex error"
```

## Supported Error Types

### Python (60+ built-in exceptions & common issues)

- `ArithmeticError` • `AssertionError` • `AttributeError` • `BlockingIOError`
- `BrokenPipeError` • `BufferError` • `ChildProcessError` • `ConnectionAbortedError`
- `ConnectionError` • `ConnectionRefusedError` • `ConnectionResetError`
- `EOFError` • `FileExistsError` • `FileNotFoundError` • `FloatingPointError`
- `ImportError` • `IndentationError` • `IndexError` • `InterruptedError`
- `IsADirectoryError` • `KeyError` • `KeyboardInterrupt` • `MemoryError`
- `ModuleNotFoundError` • `NameError` • `NotADirectoryError` • `NotImplementedError`
- `OSError` • `OverflowError` • `PermissionError` • `ProcessLookupError`
- `RecursionError` • `ReferenceError` • `RuntimeError` • `StopIteration`
- `SyntaxError` • `TabError` • `TimeoutError` • `TypeError`
- `UnboundLocalError` • `UnicodeDecodeError` • `UnicodeEncodeError`
- `ValueError` • `ZeroDivisionError` • and many more warnings (DeprecationWarning, FutureWarning, etc.)

### JavaScript / Node.js (All 7 built-in errors)

- `AggregateError` • `EvalError` • `InternalError` • `RangeError`
- `ReferenceError` • `SyntaxError` • `TypeError` • `URIError`

### TypeScript (Core compiler errors & type issues)

- Type Error (`TS2345`: not assignable) • Declaration Error (`TS2304`: cannot find name, `TS1008`: expected)
- Module Resolution (`TS2307`: cannot find module) • Interface Error (`TS2322/2324`: missing property)
- Generic Type Error (`TS2322`: constraint violated) • Union Type Error (`TS2322/2345`: not assignable)
- Async Type Error (`TS2322`: promise mismatch) • Syntax Error (`TS1003/1005`: invalid token)
- Null/Undefined Error (`TS2532/2533`: strict null checks) • Import/Export Error (`TS2305/1192`: not found)

### C / C++ (Compiler, linker & runtime)

- Syntax Error • Undefined Reference / Linker Error
- Segmentation Fault (segfault) • Null Pointer Dereference
- Type Mismatch • Array Bounds Error • Memory Leak
- Format String Mismatch • Division by Zero • Uninitialized Variable
- Include Error • Undefined Behavior

### PHP (All 16+ error levels)

- Parse Error (`E_PARSE`) • Fatal Error (`E_ERROR`) • Warning (`E_WARNING`)
- Notice (`E_NOTICE`) • Deprecated (`E_DEPRECATED`) • Type Error (`E_RECOVERABLE_ERROR`)
- Division by Zero • Out of Memory • Strict (`E_STRICT`) • Core Error (`E_CORE_ERROR`)
- Core Warning (`E_CORE_WARNING`) • Compile Error (`E_COMPILE_ERROR`)
- Compile Warning (`E_COMPILE_WARNING`) • User Error (`E_USER_ERROR`)
- User Warning (`E_USER_WARNING`) • User Notice (`E_USER_NOTICE`) • User Deprecated (`E_USER_DEPRECATED`)

### Universal / Common Errors (cross-language)

- Compilation Error • Logic Error • Runtime Error • Linkage Error
- Segmentation Fault • Network Error • Permission Error
- Timeout Error • Memory Error • Database Error
- API Key Error • SSL/Certificate Error • Input/Validation Error
- Off-by-One Error • Infinite Loop

> **Total supported error patterns:** **150+** and growing (expanded via official docs & common patterns)

## Contributing

Contribute in any way you want. You can report bugs, add patterns, write docs, or extend support for other languages. See [CONTRIBUTING.md](https://github.com/DevArqf/DeBugBuddy/blob/main/docs/CONTRIBUTING.md) for the full guide.

## Roadmap

### v0.2.0 ✅

- Typescript, C and PHP Language Support
- AI support

### v0.3.0 ❌

- Error prediction
- Custom pattern training
- GitHub integration

### v1.0.0 ❌

- 10 or more languages
- Enterprise features
- Error analytics dashboard
- Slack and Discord bots

## FAQ

**Q:** **Is my code private?**
**A:** Yes. Everything stays local unless you opt into AI mode.

**Q:** **Does it replace StackOverflow?**
**A:** For debugging, yes. You stop switching tools.

**Q:** **Can I add custom patterns?**
**A:** Yes. Edit the JSON files in `~/.debugbuddy/patterns/`.

## Support

If DeBugBuddy helps you, star the GitHub repo. Stars help other developers discover the tool.

<div align="center">
Made with ❤️ by DevArqf

Stop Googling. Understand your errors.

</div>
```