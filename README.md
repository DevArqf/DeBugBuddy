# 🐛💬 DeBugBuddy

> Your terminal's debugging companion - instant error explanations, no StackOverflow required.

DeBugBuddy is a lightweight CLI tool that helps developers understand and fix errors instantly. Think of it as ChatGPT for debugging, right in your terminal, working offline.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- 🎯 **Instant Error Explanations** - Paste an error, get a human-readable explanation
- 👁️ **Watch Mode** - Real-time error monitoring for your projects
- 📚 **Error History** - Track and learn from past errors
- 🔍 **Smart Pattern Matching** - Understands Python, JavaScript, and more
- 🤖 **Optional AI Mode** - Connect to OpenAI/Claude for advanced help
- 🚀 **Works Offline** - Core functionality needs no internet
- 🎨 **Beautiful Output** - Color-coded, formatted explanations

---

## 🚀 Quick Start

### Installation

```bash
pip install debugbuddy
```

Or install from source:

```bash
git clone https://github.com/DevArqf/DeBugBuddy
cd debugbuddy
pip install -e .
```

### Basic Usage

```bash
# Explain an error from a file
db explain error.log

# Explain an error directly
db explain "NameError: name 'x' is not defined"

# Watch a directory for errors
db watch src/

# View error history
db history

# Search for error patterns
db search "import error"
```

---

## 📖 Examples

### Example 1: Explain a Python Error

```bash
$ db explain traceback.txt

╭─────────────── 🐛 Error Explanation ────────────────╮
│ NameError                                           │
│                                                     │
│ You're using a variable or function that doesn't   │
│ exist yet.                                          │
│                                                     │
│ 💡 Fix:                                             │
│ Check that you:                                     │
│ • Spelled the name correctly                        │
│ • Defined it before using it                        │
│ • Imported it if it's from a module                 │
│                                                     │
│ Line 42                                             │
╰─────────────────────────────────────────────────────╯

💭 You've seen similar errors before
   Last time: 2024-11-20 14:30
```

### Example 2: Watch Mode

```bash
$ db watch src/

👁️  Watching src/ for python errors...
Press Ctrl+C to stop

[14:32:15] 🐛 Error detected in src/app.py
           TypeError: unsupported operand type(s) for +: 'int' and 'str'

           💡 You're trying to add different types
           Fix: Convert to same type: str(num) or int(text)
```

---

## 🎛️ Configuration

```bash
# Show current settings
db config --show

# Set AI provider
db config --set ai_provider openai
db config --set openai_api_key sk-...

# Enable verbose mode by default
db config --set verbose true

# Reset to defaults
db config --reset
```

---

## 🧩 Supported Error Types

### Python

- SyntaxError, IndentationError
- NameError, AttributeError
- TypeError, ValueError
- ImportError, ModuleNotFoundError
- IndexError, KeyError
- FileNotFoundError
- RecursionError

### JavaScript

- ReferenceError
- TypeError
- SyntaxError
- RangeError

More languages coming soon!

---

## 🤖 AI Mode (Optional)

Enable AI-powered explanations:

```bash
# Configure OpenAI
db config --set ai_provider openai
db config --set openai_api_key sk-...

# Use AI mode
db explain error.log --ai
```

Supports: OpenAI, Anthropic (Claude)

---

## 🛠️ Development

```bash
# Clone and setup
git clone https://github.com/DevArqf/DeBugBuddy
cd debugbuddy
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black debugbuddy/
```

---

## 📝 Adding Custom Patterns

Edit `debugbuddy/patterns/*.json`:

```json
{
  "type": "CustomError",
  "keywords": ["custom", "error"],
  "simple": "Simple explanation here",
  "fix": "How to fix it:\n• Step 1\n• Step 2"
}
```

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

Ideas for contributions:

- Add more language support (Go, Rust, Java)
- Improve pattern matching
- Add more error patterns
- Better AI integrations
- IDE plugins

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 🌟 Why DeBugBuddy?

- **StackOverflow is dying** - Get instant answers without leaving your terminal
- **ChatGPT context switching** - No more copy-pasting errors into browser
- **Learn as you debug** - Understand errors, don't just fix them
- **Privacy-first** - Works offline, your code stays local
- **Built by a developer, for developers**

---

## 🔗 Links

- [Documentation](https://debugbuddy.dev)
- [GitHub](https://github.com/yourusername/debugbuddy)
- [PyPI](https://pypi.org/project/debugbuddy)
- [Discord Community](https://discord.gg/debugbuddy)

---

## 💪 Roadmap

- [ ] v0.2: More language support (Go, Rust)
- [ ] v0.3: IDE plugins (VSCode, PyCharm)
- [ ] v0.4: Team error sharing
- [ ] v0.5: Error prediction
- [ ] v1.0: Local AI model support

---

**Made with ❤️ by DevArqf | Yes, I am also tired of Googling the same errors 🙄**
