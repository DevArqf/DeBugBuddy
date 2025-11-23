<div align="center">
<img width="1000" height="650" alt="DeBugBuddy Logo" src="https://github.com/DevArqf/DeBugBuddy/blob/main/DeBugBuddy%20Logo.png" />

### Your terminal’s debugging companion

Stop Googling. Understand your errors.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/pypi-v0.1.2-orange.svg)](https://pypi.org/project/debugbuddy-cli/0.1.2/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Install](#installation) •
[Quick Start](#quick-start) •
[Features](#features-screenshots) •
[Screenshots](#features-screenshots) •
[Docs](#documentation)

</div>

---

## Installation

```bash
pip install debugbuddy-cli
```

## Quick Start

```bash
db explain "NameError: name 'x' is not defined"
db explain error.log
python script.py 2>&1 | db explain
db interactive
```

### Example Output

```bash
$ db explain "NameError: name 'user_id' is not defined"

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

💡 Tip: Use db explain -e to see code examples
```

## Features-Screenshots

```bash
db
```

<img width="614" height="255" alt="db" src="https://github.com/user-attachments/assets/d468c297-bd2c-4eb9-a447-085941c71cf0" />

---

```bash
db explain "NameError: name 'user_id' is not defined"
```

<img width="1037" height="363" alt="db explain NameError" src="https://github.com/user-attachments/assets/244173c4-1b50-4c06-92cf-8e0574fdc914" />

---

```bash
db explain -e "IndexError: list index out of range"
```

<img width="1041" height="581" alt="db explain -e" src="https://github.com/user-attachments/assets/2e2f0c08-e276-48cd-a448-32f04707d876" />

---

```bash
db interactive
```

<img width="692" height="264" alt="db interactive" src="https://github.com/user-attachments/assets/8468bbe4-3fc8-4a65-b5ab-f10db2f8bd6c" />

---

```bash
[EXECUTED IN INTERACTIVE MENU] TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

<img width="740" height="470" alt="db interactive  error debug + code example" src="https://github.com/user-attachments/assets/83620a8d-7eae-4a89-a43c-0d5adbf04890" />

---

```bash
[EXECUTED IN INTERACTIVE MENU] help
```

<img width="301" height="127" alt="db interactive  help" src="https://github.com/user-attachments/assets/698a1b98-2875-4358-a159-242d0ab2f2ff" />

---

```bash
[EXECUTED IN INTERACTIVE MENU] history
```

<img width="301" height="190" alt="db interactive  history" src="https://github.com/user-attachments/assets/998acfdd-6976-4a64-9284-d756415744b0" />

---

```bash
db history
```

<img width="691" height="604" alt="db history" src="https://github.com/user-attachments/assets/807b1dbb-5240-42cd-b55d-fe812286ae58" />

---

```bash
db history --stats
```

<img width="740" height="276" alt="db history  --stats" src="https://github.com/user-attachments/assets/16f2f9bd-55e0-41be-a8b4-c4ae4b49df2e" />

---

```bash
db search "import"
```

<img width="725" height="212" alt="db search" src="https://github.com/user-attachments/assets/4cd85f05-1132-4d1b-a9a2-f9386d55cb9b" />

---

```bash
db config --show
```

<img width="710" height="307" alt="db config  --show" src="https://github.com/user-attachments/assets/6d617847-501a-4f9b-876b-b473aab9ad2e" />

## Documentation

```bash
All Commands

db explain <error>
db interactive
db watch <dir>
db history
db history --stats
db search <keyword>
db config --show
db --version
```

```bash
Extra Options

db explain -e "SyntaxError: invalid syntax"
db explain -v error.log
db watch src/ --lang javascript
db config --set ai_provider openai
db config --set openai_api_key sk-...
db explain --ai "complex error"
```

```
Supported Python Errors

- Syntax
- Indentation
- Name
- Attribute
- Type
- Value
- Import
- Module not found
- Index
- Key
- File not found
- Recursion
```

```
Supported JavaScript Errors

- Reference
- Type
- Syntax
- Range
```

```
Supported Universal Errors

- Network
- Permission
- Database
- API key
```

## Configuration

```bash
db config --show
db config --set ai_provider openai
db config --set default_language javascript
db config --reset
```

## Contributing

Contribute in any way you want. You can report bugs, add patterns, write docs, or extend support for other languages. See [CONTRIBUTING.md](https://github.com/DevArqf/DeBugBuddy/blob/main/docs/CONTRIBUTING.md) for the full guide.

## Roadmap

### v0.2.0

- Typescript, C and PHP Language Support
- VSCode extension
- Local AI support
- Team error sharing

### v0.3.0

- IDE plugins
- Error prediction
- Custom pattern training
- GitHub integration

### v1.0.0

- 10 or more languages
- Enterprise features
- Error analytics dashboard
- Slack and Discord bots

## FAQ

**Q:** **Does it work offline?**
**A:** Yes. You only need internet if you turn on optional AI mode.

**Q:** **Is my code private?**
**A:** Yes. Everything stays local unless you opt into AI mode.

**Q:** **How is this different from ChatGPT?**
**A:** It responds instantly, works offline, learns from your own history, and sits inside your terminal.

**Q:** **Does it replace StackOverflow?**
**A:** For debugging, yes. You stop switching tools.

**Q:** **Can I add custom patterns?**
**A:** Yes. Edit the JSON files in `~/.debugbuddy/patterns/`.

**Q:** **Is team use planned?**
**A:** Yes. It is on the roadmap.

## Support

If DeBugBuddy helps you, star the GitHub repo. Stars help other developers discover the tool.

<div align="center">
Made with ❤️ by DevArqf

Stop Googling. Understand your errors.

</div>
