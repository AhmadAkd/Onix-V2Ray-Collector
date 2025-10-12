# Contributing to V2Ray Config Collector

Thank you for your interest in contributing to the V2Ray Config Collector project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/V2Ray_Collector.git
cd V2Ray_Collector
```

### 2. Create a Branch

```bash
# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### 3. Make Changes

- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

### 4. Commit Changes

```bash
git add .
git commit -m "Add: brief description of your changes"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Contribution Guidelines

### Code Style

- Use Python 3.8+ syntax
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add type hints where appropriate
- Include docstrings for functions and classes

### Commit Messages

Use clear, descriptive commit messages:

```
Add: feature description
Fix: bug description
Update: change description
Remove: removal description
Docs: documentation update
```

### Testing

- Test your changes with different configurations
- Ensure the web server works correctly
- Verify automation functionality
- Check error handling

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the bug
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: 
   - Python version
   - Operating system
   - Dependencies versions
6. **Logs**: Relevant log files (remove sensitive information)

### Feature Requests

For feature requests, please include:

1. **Description**: Clear description of the feature
2. **Use Case**: Why this feature would be useful
3. **Proposed Solution**: How you think it should work
4. **Alternatives**: Any alternative solutions considered

## 🚀 Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/AhmadAkd/V2Ray_Collector.git
cd V2Ray_Collector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests

```bash
# Run basic functionality test
python config_collector.py

# Run web server test
python web_server.py --debug

# Run automation test
python automation.py --mode once
```

## 📁 Project Structure

```
V2Ray_Collector/
├── config_collector.py      # Main collection engine
├── automation.py            # Automation system
├── web_server.py           # Web server
├── config.py              # Configuration
├── start.py               # Quick start
├── requirements.txt       # Dependencies
├── README.md             # Persian docs
├── README_EN.md          # English docs
├── CONTRIBUTING.md       # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore rules
```

## 🔧 Configuration

### Development Configuration

For development, you can modify `config.py`:

```python
# Change to development profile
ACTIVE_PROFILE = 'development'

# Or modify specific settings
COLLECTION_CONFIG['max_concurrent_tests'] = 10
AUTOMATION_CONFIG['collection_interval_minutes'] = 5
```

### Adding New Sources

To add new configuration sources:

1. Add the URL to `CONFIG_SOURCES` in `config.py`
2. Test the source manually
3. Ensure the format is compatible
4. Update documentation

### Adding New Protocols

To support new protocols:

1. Add protocol info to `SUPPORTED_PROTOCOLS` in `config.py`
2. Implement parser in `config_collector.py`
3. Add test cases
4. Update documentation

## 🌐 Internationalization

### Adding New Languages

To add support for new languages:

1. Create `README_[LANG].md` file
2. Update web server templates
3. Add language-specific strings
4. Update documentation

### Persian/English Support

The project supports both Persian and English:

- `README.md` - Persian documentation
- `README_EN.md` - English documentation
- Web interface - Both languages supported

## 🔒 Security

### Security Guidelines

- Never commit sensitive information (API keys, passwords, etc.)
- Use environment variables for sensitive data
- Validate all input data
- Follow secure coding practices
- Report security vulnerabilities privately

### Reporting Security Issues

For security issues, please:

1. **DO NOT** create a public issue
2. Email security concerns to: security@example.com
3. Include detailed information about the vulnerability
4. Allow time for response before public disclosure

## 📝 Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Provide screenshots for UI changes
- Keep documentation up to date
- Use consistent formatting

### Updating Documentation

When making changes:

1. Update relevant documentation files
2. Include usage examples
3. Update README files if needed
4. Add comments to complex code

## 🎯 Areas for Contribution

### High Priority

- Performance optimizations
- Additional protocol support
- Better error handling
- Enhanced web interface
- Mobile app integration

### Medium Priority

- Docker containerization
- CI/CD pipeline
- Automated testing
- Performance monitoring
- Additional language support

### Low Priority

- Advanced analytics
- User management
- API authentication
- Third-party integrations
- Advanced filtering

## 🏆 Recognition

Contributors will be recognized in:

- README contributors section
- Release notes
- Project documentation
- GitHub contributors page

## 📞 Getting Help

### Community Support

- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Email for private matters

### Code Review Process

1. All contributions require review
2. Maintainers will review within 48 hours
3. Address feedback promptly
4. Ensure tests pass
5. Maintain code quality standards

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Thank you for contributing to the V2Ray Config Collector project! Your contributions help make this tool better for everyone in the V2Ray community.

---

**Note**: This is a community-driven project. Please be respectful and constructive in all interactions.
