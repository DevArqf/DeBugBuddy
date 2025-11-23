# Contributing to DeBugBuddy

Thanks for taking the time to improve DeBugBuddy. Your work helps developers fix problems faster and stay focused in their terminal.

## Quick Start

```bash
1. Fork the repo
2. Clone your fork
   `git clone https://github.com/DevArqf/DeBugBuddy`
3. Create a branch
   `git checkout -b feature/amazing-feature`
4. Make your changes
5. Run the tests
   `pytest`
6. Commit
   `git commit -m 'Add amazing feature'`
7. Push
   `git push origin feature/amazing-feature`
8. Open a pull request
```

## Found a Bug?

Before you open an issue:

- Check existing issues
- Update your version
  `pip install --upgrade debugbuddy`

When you report a bug, be clear:

- Explain what you expected
- Explain what happened
- Share error messages
- Share your OS and Python version
- Provide steps to reproduce the bug

Use this template:

```
Bug Description
Clear description of the bug

To Reproduce
1. Run `db explain "..."`
2. See error

Expected Behavior
What should happen

Environment
- OS: macOS 13.0
- Python: 3.10.0
- DeBugBuddy: 0.1.2

Additional Context
Any other info
```

## Want to Add a Feature?

Before you start:

- Check the roadmap
- Open an issue and describe your idea
- Make sure no one is already working on it

Popular feature ideas:

- New error patterns
- Language support
- Clearer explanations
- UI improvements
- Performance updates
- Documentation fixes

## Adding Error Patterns

This is one of the fastest ways to improve DeBugBuddy.

### 1. Find the Pattern File

- Python: `debugbuddy/patterns/python.json`
- JavaScript: `debugbuddy/patterns/javascript.json`
- Universal: `debugbuddy/patterns/common.json`

### 2. Add a Pattern

```json
{
  "type": "YourErrorType",
  "keywords": ["keyword1", "keyword2"],
  "simple": "Simple explanation in plain English",
  "fix": "How to fix:\n  • Step 1\n  • Step 2\n  • Step 3",
  "example": "# Wrong\ncode\n\n# Right\nworking code",
  "did_you_mean": ["Suggestion 1", "Suggestion 2"]
}
```

### 3. Follow These Rules

Simple explanation:

- Start with a magnifying glass
- Use plain language
- Explain the cause
- Keep a helpful tone

Fix section:

- Give two or three clear steps
- Use bullets
- Add code if needed

Example section:

- Show failing code
- Show working code
- Keep it short

### 4. Test It

```
db explain "your error type here"
```

## Adding Language Support

### 1. Create a Pattern File

`debugbuddy/patterns/your_language.json`

```json
{
  "language": "your_language",
  "version": "1.0",
  "errors": [
    {
      "type": "CompileError",
      "keywords": ["..."],
      "simple": "...",
      "fix": "...",
      "example": "..."
    }
  ]
}
```

### 2. Add the Parser

In `debugbuddy/core/parser.py`:

```python
def _parse_your_language(self, text: str):
    """Parse YourLanguage errors"""
    pass
```

### 3. Add Tests

Update `tests/test_parser.py`

### 4. Update the Docs

Add the language under Supported Errors in the README.

## Improving the CLI

Follow these style rules:

- Use Python 3.8+
- Follow PEP 8
- Add type hints
- Write docstrings
- Keep functions short

Interface rules:

- Use Rich for formatting
- Keep colors consistent
- Test on different terminal sizes

## Testing

```
pytest
pytest --cov=debugbuddy
pytest tests/test_parser.py
```

### Write Tests

```python
def test_your_feature():
    input_data = "..."
    result = your_function(input_data)
    assert result == expected_output
```

## Documentation

```python
def explain_error(error: str) -> Dict:
    """
    Explain a programming error in plain English.
    """
    pass
```

### README

- Keep examples current
- Add new features
- Update screenshots
- Fix typos

## Contribution Ideas

### Good First Issues

- Add error patterns
- Fix typos
- Improve messages
- Add tests
- Update examples

### Intermediate

- Add language support
- Improve pattern detection
- Add CLI features
- Improve formatting
- Optimize code

### Advanced

- Improve AI integration
- Add local model support
- Build IDE plugins
- Add team features
- Build analytics tools

## Communication

Questions: open a GitHub Discussion
Bugs: open an Issue

### Standards

Do:

- Be respectful
- Give clear feedback
- Help others learn
- Support contributions

Don't:

- Harass
- Exclude
- Share private info
- Act unprofessionally

Report issues: [devarqf@gmail.com](mailto:devarqf@gmail.com)

## Recognition

Contributors receive:

- A spot in the README
- Release note mentions
- Public thanks

Top contributors:

- Ten or more PRs: Core Contributor badge
- Fifty or more PRs: Maintainer status
- Pattern authors: Credit in pattern files

## Pull Request Checklist

- Code follows guidelines
- Tests pass
- New tests added where needed
- Docs updated
- Commits are clear
- No conflicts
- Related issues linked

## Release Process

For maintainers:

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release branch
4. Run tests
5. Build
   `python setup.py sdist bdist_wheel`
6. Upload to TestPyPI
   `twine upload --repository testpypi dist/*`
7. Upload to PyPI
8. Create GitHub release
9. Publish announcement

## FAQ

**I’m new to open source. Where do I start?**
Start with issues marked as good first issue. Adding patterns is a strong first step.

**How fast are reviews?**
Reviews usually happen within forty eight hours.

**Can I work on multiple issues?**
Yes. Keep each pull request focused.

**My PR was rejected. What now?**
Read the feedback and update the PR. The process is part of learning the codebase.

**How do I become a maintainer?**
Contribute often and show you understand the structure. I’ll reach out when the time is right.

## Thank You

Every contribution strengthens DeBugBuddy.
Thanks for helping developers debug with more confidence.
