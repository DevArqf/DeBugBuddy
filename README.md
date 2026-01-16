<div align="center">
<img width="720" alt="DeBugBuddy Logo" src="https://raw.githubusercontent.com/DevArqf/DeBugBuddy/main/DeBugBuddy%20Logo.png" />

### Your terminal's debugging companion

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/debugbuddy-cli.svg)](https://pypi.org/project/debugbuddy-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/debugbuddy-cli.svg)](https://pypi.org/project/debugbuddy-cli/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Install](#installation) • [Quick Start](#quick-start) • [Commands](#commands) • [TUI](#tui-textual-gui) • [Docs](https://debugbuddy.vercel.app) • [Roadmap](#roadmap)

</div>

## Overview
DeBugBuddy is an open-source CLI + TUI that explains errors in plain English, predicts issues before they break, and keeps a searchable local history. It runs locally by default for privacy and supports multiple languages with extensible pattern libraries.

## Why DeBugBuddy
- **Faster debugging**: See the cause and fix without searching the web.
- **Predictive checks**: Catch likely errors in a file before running it.
- **Local-first privacy**: AI is opt-in, not required.
- **History & analytics**: Track frequent errors and languages over time.
- **TUI workflow**: Full-screen [Textual GUI](https://textual.textualize.io/) for focused debugging.

## Screenshots

- **TUI dashboard**
  ![TUI dashboard](https://raw.githubusercontent.com/DevArqf/DeBugBuddy/main/docs-static/assets/tui-hero.png)
- **Explain view**
  ![Explain view](https://raw.githubusercontent.com/DevArqf/DeBugBuddy/main/docs-static/assets/tui-explain.png)
- **Predict view**
  ![Predict view](https://raw.githubusercontent.com/DevArqf/DeBugBuddy/main/docs-static/assets/tui-predict.png)
- **History analytics**
  ![History analytics](https://raw.githubusercontent.com/DevArqf/DeBugBuddy/main/docs-static/assets/tui-history.png)

## Installation

```bash
pip install debugbuddy-cli
```

## Quick Start

```bash
# Explain an error
python script.py
dbug explain

# Predict errors in a file
dbug predict app.py

# View history and stats
dbug history --stats

# Launch the full-screen GUI
debugbuddy
```

## Commands

```bash
All Commands

dbug explain     Explain an error message
dbug predict     Predict errors in a file
dbug watch       Watch files for errors
dbug history     View error history
dbug train       Train custom patterns or ML models
dbug search      Search error patterns
dbug config      Manage configuration
dbug github      GitHub integration
```

## TUI (Textual GUI)
Run the GUI and switch between commands without leaving the terminal:

```bash
debugbuddy
```

- Use the left sidebar to switch between Explain, Predict, History, Search, Config, GitHub, Watch, and Train commands.
- Results stay in the TUI so you can keep iterating without reopening.

## AI Providers
AI is optional and opt-in. Set a provider and API key:

```bash
dbug config ai_provider grok

dbug config grok_api_key YOUR_KEY
```

Supported providers:
- OpenAI
- Anthropic
- Grok

## GitHub Search Accuracy
Use repo scoping and exact matching for precision:

```bash
dbug github search "TypeError: unsupported operand type(s) for +" \
  -l python --repo yourorg/yourrepo --exact --include-closed
```

## Supported Languages
- Python, JavaScript, TypeScript, C/C++, PHP, Java and Ruby

> **Total supported error patterns:** **150+** and growing.

## Configuration
All settings are stored locally in `~/.debugbuddy/config.json`.
Common settings:
- `ai_provider`
- `openai_api_key` / `anthropic_api_key` / `grok_api_key`
- `use_ml_prediction`
- `max_history`

## Contributing
Contributions are welcome. You can report bugs, add patterns, improve docs, or add new languages.
See [CONTRIBUTING.md](https://github.com/DevArqf/DeBugBuddy/blob/main/docs/CONTRIBUTING.md).

## Roadmap

### v0.2.0 ✅
- [x] Typescript, C and PHP Language Support
- [x] AI support

### v0.3.0 ✅
- [x] Error prediction
- [x] Custom pattern training
- [x] GitHub integration

### v0.4.0 (Q1 2026) ✅
- [x] Java and Ruby Language Support
- [x] ML prediction optimization for faster inference (e.g., model quantization, caching improvements).
- [x] Introduce basic error analytics in CLI (e.g., stats on frequent errors from history).
- [x] Introduce Grok as an AI Provider for the AI Mode.
- [x] Full test coverage for new languages; refactor pattern manager for easier additions.

### v0.5.0 (Q2 2026) ❌
- [ ] Go and Rust Language Support
- [ ] Implement IDE integrations (e.g., VS Code extension for seamless CLI calls).
- [ ] Improve custom training with user-friendly wizards and example datasets.
- [ ] Add multi-file/project scanning for prediction/watch.
- [ ] Security audit and fixes (e.g., safe error message parsing to prevent injection).

### v0.6.0 (Q3 2026) ❌
- [ ] Introduce a basic web-based error analytics dashboard (e.g., using Flask/Dash; local server mode) for visualizing history, patterns, and predictions.
- [ ] Swift Language Support
- [ ] Enable export/import of patterns and history (e.g., JSON/CSV).
- [ ] Introduce performance benchmarks and optimizations for large projects.
- [ ] Community features: Template for contributing new language patterns.

### v0.7.0 (Q3 2026) ❌
- [ ] Kotlin and C# Language Support
- [ ] Implement Slack bot for error explanations/predictions (e.g., slash commands to query from chat).
- [ ] Enhance dashboard with interactive charts (e.g., error frequency over time, language breakdowns).
- [ ] Add collaborative mode (e.g., share prediction reports via links).
- [ ] Extensive documentation updates, including API reference for extensions.

### v0.8.0 (Q4 2026) ❌
- [ ] Implement Discord bot with similar features to Slack (e.g., error queries, notifications).
- [ ] Dashboard enhancements: User authentication, cloud sync option (opt-in for privacy).
- [ ] Introduce advanced ML features (e.g., auto-suggest fixes based on history).

### v0.9.0 (Q4 2026) ❌
- [ ] Scala and Elixir Language Support
- [ ] Full integration testing for dashboard.
- [ ] Performance profiling and optimizations (e.g., reduce startup time <1s).
- [ ] User feedback loop: Add in-app surveys or GitHub issue templates.

### v1.0.0 (Q1 2027) ❌
- [ ] Official support for 12+ languages.
- [ ] Fully featured error analytics dashboard (local/web, with visualizations and exports).
- [ ] Slack and Discord bots support for real-time debugging assistance.

> **Q** stands for quarter: Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec).

## FAQ

**Q: Is my code private?**  
**A:** Yes. Everything stays local unless you opt into AI mode.

**Q: Does it replace StackOverflow?**   
**A:** For debugging, yes. You stop switching tools.

**Q: Can I add custom patterns?**   
**A:** Yes. Edit the JSON files in `./patterns`.

## Support
If DeBugBuddy helps you, star the GitHub repo. Stars help other developers discover the tool.
