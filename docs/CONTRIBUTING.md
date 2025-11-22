# 🤝 Contributing to DeBugBuddy

First off, **thank you** for considering contributing to DeBugBuddy! This project is built by DevArqf, for developers. Every contribution helps make debugging easier for everyone.

---

## 🎯 Quick Start

1. Fork the repo
2. Clone your fork: `git clone https://github.com/DevArqf/DeBugBuddy`
3. Create a branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Test: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

---

## 🐛 Found a Bug?

**Before creating an issue:**

- Check if it's already reported
- Make sure you're on the latest version: `pip install --upgrade debugbuddy`

**When reporting:**

- Describe what you expected
- Describe what actually happened
- Include error messages
- Share your OS and Python version
- Provide steps to reproduce

**Use this template:**

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**

1. Run `db explain "..."`
2. See error

**Expected Behavior**
What should happen

**Environment**

- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.10.0]
- DeBugBuddy: [e.g., 0.1.0]

**Additional Context**
Any other info
```

---

## ✨ Want to Add a Feature?

**Before starting:**

- Check the [roadmap](README.md#roadmap)
- Open an issue to discuss your idea
- Make sure no one else is working on it

**Feature ideas we love:**

- New error patterns
- Language support
- Better explanations
- UI improvements
- Performance optimizations
- Documentation

---

## 📝 Adding Error Patterns

This is the **easiest and most valuable** way to contribute!

### 1. Find the Right File

- Python errors: `debugbuddy/patterns/python.json`
- JavaScript errors: `debugbuddy/patterns/javascript.json`
- Universal errors: `debugbuddy/patterns/common.json`

### 2. Add Your Pattern

```json
{
  "type": "YourErrorType",
  "keywords": ["keyword1", "keyword2"],
  "simple": "🔍 Simple explanation in plain English",
  "fix": "How to fix:\n  • Step 1\n  • Step 2\n  • Step 3",
  "example": "# ❌ Wrong\ncode that fails\n\n# ✅ Correct\nworking code",
  "did_you_mean": ["Suggestion 1", "Suggestion 2"]
}
```

### 3. Follow These Guidelines

**Simple Explanation:**

- Start with 🔍
- Use plain English
- Be encouraging, not condescending
- Explain WHY it happens

**Fix:**

- Provide 2-3 actionable solutions
- Use bullet points
- Include code if helpful

**Example:**

- Show wrong code (❌)
- Show correct code (✅)
- Use realistic examples
- Keep it short (< 10 lines)

### 4. Test It

```bash
db explain "your error type here"
```

---

## 🌍 Adding Language Support

Want to add Go, Rust, Java, or another language?

### 1. Create Pattern File

`debugbuddy/patterns/your_language.json`:

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

### 2. Add Parser Support

In `debugbuddy/core/parser.py`, add detection:

```python
def _parse_your_language(self, text: str) -> Optional[Dict]:
    """Parse YourLanguage errors"""
    # Add parsing logic
    pass
```

### 3. Update Tests

Add test cases in `tests/test_parser.py`

### 4. Update Documentation

Add language to README.md under "Supported Errors"

---

## 🎨 Improving the CLI

### Code Style

- Use Python 3.8+ features
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small

### UI Guidelines

- Use Rich library for formatting
- Keep colors consistent:
  - Red: errors
  - Green: success
  - Yellow: warnings
  - Cyan: info
- Add emojis for visual appeal
- Test on different terminal sizes

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=debugbuddy

# Specific test
pytest tests/test_parser.py
```

### Write Tests

```python
def test_your_feature():
    """Test description"""
    # Arrange
    input_data = "..."

    # Act
    result = your_function(input_data)

    # Assert
    assert result == expected_output
```

---

## 📚 Documentation

### Code Comments

```python
def explain_error(error: str) -> Dict:
    """
    Explain a programming error in plain English.

    Args:
        error: The error message to explain

    Returns:
        Dict containing explanation and fix

    Example:
        >>> explain_error("NameError: name 'x' is not defined")
        {'simple': '...', 'fix': '...'}
    """
    pass
```

### README Updates

- Keep examples up to date
- Add new features to feature list
- Update screenshots if UI changes
- Fix typos and improve clarity

---

## 🎯 Contribution Ideas

### 🟢 Good First Issues

Perfect for newcomers:

- Add new error patterns
- Fix typos in documentation
- Improve error messages
- Add tests for existing features
- Update README examples

### 🟡 Intermediate

Need some experience:

- Add language support
- Improve pattern matching
- Enhance CLI output
- Add new commands
- Optimize performance

### 🔴 Advanced

For experienced developers:

- AI integration improvements
- Local LLM support
- IDE plugins
- Team collaboration features
- Analytics dashboard

---

## 💬 Communication

- **Questions:** Open a [GitHub Discussion](https://github.com/DevArqf/DeBugBuddy/discussions)
- **Bugs:** Create an [Issue](https://github.com/DevArqf/DeBugBuddy/issues)

---

## 📜 Code of Conduct

### Our Pledge

I'm committed to making DeBugBuddy welcoming to everyone.

### Our Standards

✅ **DO:**

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Celebrate contributions

❌ **DON'T:**

- Harass or discriminate
- Use inappropriate language
- Share others' private info
- Act unprofessionally

### Enforcement

Report issues to: conduct@debugbuddy.dev

---

## 🎉 Recognition

Contributors get:

- Listed in README
- Mentioned in release notes
- Our eternal gratitude! 🙏

Top contributors:

- **10+ PRs:** Core Contributor badge
- **50+ PRs:** Maintainer status
- **Pattern authors:** Credit in pattern files

---

## 📋 Pull Request Checklist

Before submitting:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] Commits are well-described
- [ ] No merge conflicts
- [ ] Linked related issues

---

## 🚀 Release Process

(For maintainers)

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release branch
4. Run full test suite
5. Build: `python setup.py sdist bdist_wheel`
6. Test on PyPI test: `twine upload --repository testpypi dist/*`
7. Upload to PyPI: `twine upload dist/*`
8. Create GitHub release
9. Announce on social media

---

## ❓ FAQ

**Q: I'm new to open source. Where do I start?**  
A: Look for issues labeled `good first issue`. Adding error patterns is a great way to start!

**Q: How long until my PR is reviewed?**  
A: Usually within 48 hours. Be patient!

**Q: Can I work on multiple issues?**  
A: Yes, but focus on one PR at a time for faster reviews.

**Q: My PR was rejected. Now what?**  
A: Don't worry! Address the feedback and resubmit. I'm here to help.

**Q: How do I become a maintainer?**  
A: Contribute consistently and show you understand the codebase. I'll reach out!

---

## 🙏 Thank You!

Every contribution, no matter how small, makes DeBugBuddy better.

**Thank you for helping developers debug smarter!** 🐛💬
