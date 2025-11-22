<div align="center">

<img width="1000" height="650" alt="DeBugBuddy Logo" src="https://github.com/DevArqf/DeBugBuddy/blob/main/DeBugBuddy%20Logo.png" />

### _Your terminal's debugging companion_

**Stop Googling. Start Understanding.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/pypi-v0.1.0-orange.svg)](https://pypi.org/project/debugbuddy/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Install](#-installation) •
[Quick Start](#-quick-start) •
[Features](#-features) •
[Screenshots](#-screenshots) •
[Docs](#-documentation)

</div>

---

## 🤔 The Problem

You know the drill:

1. Code breaks
2. Copy error to ChatGPT
3. Wait for response
4. Switch back to terminal
5. Try fix
6. Repeat...

**Sound familiar?** You're not alone. Developers waste **hours every day** context-switching between their code and AI tools.

---

## ✨ The Solution

**DeBugBuddy** is ChatGPT for debugging, but:

- ⚡ **Instant** - No API calls, no waiting
- 🔒 **Private** - Your code stays local
- 🎯 **Smart** - Knows 100+ error patterns
- 💬 **Interactive** - Chat mode for complex issues
- 📚 **Learning** - Get better explanations each time

---

## 🚀 Installation

```bash
pip install debugbuddy
```

That's it. You're ready to debug smarter.

---

## 🎯 Quick Start

### Basic Usage

```bash
# Explain any error
db explain "NameError: name 'x' is not defined"

# From a file
db explain error.log

# From your terminal
python script.py 2>&1 | db explain

# Interactive mode
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

---

## 🎨 Features

### 🎯 **Instant Error Explanations**

No more copying errors to ChatGPT. Get human-readable explanations in < 1 second.

```bash
db explain "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

### 💬 **Interactive Chat Mode** 🔥 _NEW_

Talk to DeBugBuddy about your errors. It remembers context.

```bash
db interactive

You: [paste error]
🐛 DeBugBuddy: This is a NameError...
You: how do I fix it?
🐛 DeBugBuddy: Here are 3 ways...
```

### 🧠 **Smart Suggestions** 🔥 _NEW_

"Did you mean...?" suggestions for common typos.

```bash
NameError: name 'pint' is not defined

💡 Did you mean?
  • print
  • int
  • point
```

### 📝 **Code Examples** 🔥 _NEW_

See working examples for every error type.

```bash
db explain -e "IndexError: list index out of range"

📚 Example:
# ❌ Wrong
fruits = ['apple', 'banana']
print(fruits[5])  # Only 2 items!

# ✅ Correct
if len(fruits) > 5:
    print(fruits[5])
```

### 👁️ **Watch Mode**

Real-time error monitoring while you code.

```bash
db watch src/

[14:32:15] 🐛 Error detected in app.py
           TypeError: Cannot add int + str
           💡 Convert types first
```

### 📚 **Error History**

Learn from your mistakes. Track patterns over time.

```bash
db history --stats

📊 Your Debugging Statistics
Total errors: 47
Most common: NameError (12x)
```

### 🔍 **Pattern Search**

Find solutions for errors you haven't seen yet.

```bash
db search "import"

Found 3 patterns:
1. ImportError - Module not found
2. ModuleNotFoundError - Package missing
3. ImportWarning - Deprecated import
```

---

## 📸 Screenshots
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

---

### Before DeBugBuddy

```
1. See error
2. Copy to ChatGPT
3. Wait...
4. Read response
5. Go back to terminal
6. Try fix
7. Error again...
```

⏱️ **Time wasted: 5-10 minutes per error**

### After DeBugBuddy

```
1. db explain [paste error]
2. See instant fix
3. Apply solution
4. Done
```

⏱️ **Time saved: 90%**

---

## 📚 Documentation

### All Commands

```bash
db explain <error>       # Explain any error
db interactive          # Start chat mode
db watch <dir>          # Monitor directory
db history              # View past errors
db history --stats      # Show statistics
db search <keyword>     # Search patterns
db config --show        # View settings
db --version            # Show version
```

### Advanced Usage

**With code examples:**

```bash
db explain -e "SyntaxError: invalid syntax"
```

**Verbose mode:**

```bash
db explain -v error.log
```

**Watch specific language:**

```bash
db watch src/ --lang javascript
```

**AI mode (requires API key):**

```bash
db config --set ai_provider openai
db config --set openai_api_key sk-...
db explain --ai "complex error"
```

---

## 🛠️ Supported Errors

### Python

✅ SyntaxError, IndentationError  
✅ NameError, AttributeError  
✅ TypeError, ValueError  
✅ ImportError, ModuleNotFoundError  
✅ IndexError, KeyError  
✅ FileNotFoundError  
✅ RecursionError

### JavaScript

✅ ReferenceError  
✅ TypeError  
✅ SyntaxError  
✅ RangeError

### Universal

✅ Network Errors  
✅ Permission Errors  
✅ Database Errors  
✅ API Key Errors

**More languages coming soon!** (Go, Rust, Java)

---

## 🎨 Configuration

Customize DeBugBuddy to your workflow:

```bash
# View all settings
db config --show

# Enable AI mode
db config --set ai_provider openai

# Change default language
db config --set default_language javascript

# Reset everything
db config --reset
```

---

## 🤝 Contributing

I love anyone and everyone with their contributions! DeBugBuddy is built by DevArqf, for developers.

**Ways to contribute:**

- 🐛 Report bugs
- ✨ Suggest features
- 📝 Improve error patterns
- 🌍 Add language support
- 📚 Write documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 🗺️ Roadmap

### v0.2.0 (Next Month)

- [ ] Go, Rust, Java support
- [ ] VSCode extension
- [ ] Local AI model support
- [ ] Team error sharing

### v0.3.0

- [ ] IDE plugins (PyCharm, IntelliJ)
- [ ] Error prediction
- [ ] Custom pattern training
- [ ] GitHub integration

### v1.0.0

- [ ] Multi-language support (10+ languages)
- [ ] Enterprise features
- [ ] Error analytics dashboard
- [ ] Slack/Discord bots

**Want to influence the roadmap?** [Vote on features →](https://github.com/DevArqf/DeBugBuddy/discussions)

---

## ❓ FAQ

**Q: Does it work offline?**  
A: Yes! Core features work without internet. AI mode is optional.

**Q: Is my code private?**  
A: 100%. Everything runs locally unless you enable AI mode.

**Q: How is this different from ChatGPT?**  
A: Instant (no API calls), works offline, learns from YOUR errors, context-aware.

**Q: Does it replace StackOverflow?**  
A: For debugging, pretty much. You'll rarely need to search anymore.

**Q: Can I add custom patterns?**  
A: Yes! Edit the JSON files in `~/.debugbuddy/patterns/`

**Q: What about enterprise/team use?**  
A: That feature is currently being worked on.

---

## 📊 Stats

- **100+** error patterns built-in
- **3** languages supported (Python, JavaScript, Universal)
- **< 1 second** average response time
- **90%** reduction in debug time
- **100%** privacy (runs locally)

---

## 🙏 Acknowledgments

Built with:

- [Click](https://click.palletsprojects.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Watchdog](https://python-watchdog.readthedocs.io/) - File monitoring

Inspired by every developer who's ever said _"I just Googled this same error yesterday"_

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🌟 Show Your Support

If DeBugBuddy saves you time, give it a ⭐ on GitHub!

Every star helps other developers discover it.

[![GitHub stars](https://img.shields.io/github/stars/DevArqf/DeBugBuddy?style=social)](https://github.com/DevArqf/DeBugBuddy)

---

<div align="center">

**Made with ❤️ by DevArqf | Yes, I am also tired of Googling the same errors 🙄**

_Stop Googling. Start Understanding._

[⬆ Back to top](#-debugbuddy)

</div>
