# Contributing to Electronic Module Template

We welcome contributions to improve this electronic module documentation template! This guide will help you get started with contributing to the project.

## How to Contribute

### 1. Fork and Clone

1. Fork this repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/electronic-module-template.git
   cd electronic-module-template
   ```

### 2. Set Up Development Environment

1. Ensure you have the required tools:
   - Python 3.8+
   - LaTeX distribution (TeX Live recommended)
   - Git

2. Install Python dependencies:
   ```bash
   cd info/scripts/
   pip install -r requirements.txt
   ```

### 3. Make Your Changes

#### Documentation Improvements
- Update templates in `info/templates/`
- Improve metadata structure in `info/metadata/`
- Enhance scripts in `info/scripts/`

#### Hardware Documentation
- Update hardware specifications in `hardware/README.md`
- Add or improve hardware resources in `hardware/resources/`

#### Software Examples
- Improve C examples in `software/examples/c/`
- Enhance Python examples in `software/examples/python/`

### 4. Test Your Changes

1. Test documentation generation:
   ```bash
   cd info/scripts/
   python generate_docs.py
   ```

2. Verify path configuration:
   ```bash
   python path_config.py
   ```

3. Check that PDF generation works correctly

### 5. Submit Your Contribution

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: your descriptive commit message"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request on GitHub

## Contribution Guidelines

### Code Style
- Use clear, descriptive variable names
- Add comments for complex logic
- Follow PEP 8 for Python code
- Use consistent formatting

### Documentation
- Update README.md if you change functionality
- Add inline documentation for new functions
- Include examples for new features

### Commit Messages
Use clear commit messages that describe what was changed:
- `Add: new feature or file`
- `Fix: bug fix`
- `Update: modification to existing feature`
- `Remove: deletion of feature or file`
- `Docs: documentation changes`

### Testing
- Test your changes on multiple systems if possible
- Ensure PDF generation works correctly
- Verify that all paths resolve correctly

## Types of Contributions Welcome

### 🐛 Bug Reports
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, LaTeX distribution)

### 💡 Feature Requests
- Clear description of the proposed feature
- Explanation of why it would be useful
- Possible implementation approach

### 📚 Documentation
- Improvements to README files
- Better code comments
- Tutorial enhancements
- Translation improvements

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring

## Project Structure

Understanding the project structure will help you contribute effectively:

```
.
├── docs/                    # Generated documentation
├── info/                    # Project metadata and scripts
│   ├── metadata/           # Configuration files
│   ├── scripts/            # Build and utility scripts
│   └── templates/          # LaTeX templates
├── hardware/               # Hardware documentation
│   ├── README.md          # Hardware specifications
│   └── resources/         # Images and resources
├── software/               # Software examples
│   └── examples/          # Code examples
├── README.md              # Main project README
├── LICENSE                # Project license
└── CONTRIBUTING.md        # This file
```

## Development Workflow

1. **Setup**: Fork and clone the repository
2. **Plan**: Create an issue or discuss your idea
3. **Develop**: Make your changes in a feature branch
4. **Test**: Ensure everything works correctly
5. **Document**: Update documentation as needed
6. **Submit**: Create a pull request

## Getting Help

If you need help contributing:

1. Check existing issues and documentation
2. Create a new issue with your question
3. Be specific about what you're trying to do
4. Include relevant system information

## Recognition

Contributors will be recognized in:
- Project README.md
- Release notes for significant contributions
- Project documentation

Thank you for contributing to the Electronic Module Template! 🚀

---

*This contributing guide is part of the Electronic Module Template project.*
