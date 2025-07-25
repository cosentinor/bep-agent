# Contributing to BEP Agent

Thank you for your interest in contributing to BEP Agent! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bep-agent.git
   cd bep-agent
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run tests** to ensure everything works:
   ```bash
   python test_installation.py
   python demo_simple.py
   ```

## 🛠️ Development Setup

### Environment Setup
1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
2. Add your OpenAI API key (optional for development)
3. Set `USE_LOCAL_EMBEDDINGS=true` for development without API costs

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Testing
- Test your changes with `python test_installation.py`
- Ensure the simple demo works: `python demo_simple.py`
- Test the full application: `streamlit run main.py`

## 📝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Provide clear description of the problem
- Include steps to reproduce
- Add relevant error messages or logs

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Provide examples of how it would be used

### Submitting Changes
1. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** with clear, focused commits
3. **Test thoroughly** to ensure nothing breaks
4. **Update documentation** if needed
5. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots if UI changes

## 🎯 Areas for Contribution

### High Priority
- **PDF Support**: Add support for PDF document processing
- **Template System**: Create customizable BEP templates
- **Performance**: Optimize vector search and generation speed
- **Testing**: Add comprehensive unit and integration tests

### Medium Priority
- **UI/UX**: Improve the Streamlit interface
- **Export Formats**: Add Word document export
- **Collaboration**: Multi-user features
- **Analytics**: Usage tracking and metrics

### Documentation
- **Tutorials**: Step-by-step guides for different use cases
- **API Documentation**: Detailed function and class documentation
- **Examples**: More sample projects and use cases
- **Video Guides**: Screen recordings of the workflow

## 🔧 Technical Guidelines

### Code Organization
- Keep modules focused on single responsibilities
- Use type hints where possible
- Handle errors gracefully with informative messages
- Log important operations for debugging

### Dependencies
- Minimize new dependencies
- Use well-maintained, popular packages
- Update requirements.txt for new dependencies
- Consider optional dependencies for advanced features

### Performance
- Profile code for bottlenecks
- Use efficient algorithms and data structures
- Consider memory usage for large documents
- Implement caching where appropriate

## 📋 Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have appropriate tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive information (API keys, etc.) is committed
- [ ] Changes are backwards compatible (or breaking changes are documented)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional tone in all interactions

## 📞 Getting Help

- **Questions**: Open a GitHub issue with the "question" label
- **Discussions**: Use GitHub Discussions for broader topics
- **Documentation**: Check existing docs before asking

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor graphs

Thank you for helping make BEP Agent better! 🏗️
