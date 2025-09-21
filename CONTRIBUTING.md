# Contributing to Lithium-Validation

Thank you for your interest in contributing to Lithium-Validation! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/GED-DO/Lithium-Validation/issues)
2. Create a new issue using the bug report template
3. Include:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information

### Suggesting Features

1. Check existing feature requests
2. Create a new issue using the feature request template
3. Describe the feature and its use case

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Run tests (`pytest`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/GED-DO/Lithium-Validation.git
cd Lithium-Validation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black lithium_validation tests

# Type checking
mypy lithium_validation
```

## Code Standards

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for all public functions
- Add tests for new features
- Keep commits atomic and descriptive

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features

## Questions?

Feel free to open an issue for any questions about contributing.

## Author

Guillermo Espinosa (hola@ged.do)
