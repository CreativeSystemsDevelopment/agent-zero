# Changelog

All notable changes to the OpenRouter Model Fetcher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-10

### Added
- Initial release of OpenRouter Model Fetcher
- Configuration management system with environment variable support
- OpenRouter API client with comprehensive error handling
- Automatic retry logic with exponential backoff
- Data processing pipeline for model information
- Multiple output formatters (Markdown, JSON, CSV)
- File-based caching system with TTL support
- Command-line interface with argparse
- Filtering capabilities:
  - Filter by tags
  - Search by name or description
  - Filter by minimum context length
- Statistics calculation:
  - Total model count
  - Models by modality
  - Unique tags
  - Average and maximum context lengths
- Comprehensive logging to both console and file
- Debug mode for detailed troubleshooting
- Force refresh option to bypass cache
- Custom output file path support
- README with complete documentation
- EXAMPLES.md with usage scenarios
- Shell script for convenient execution
- .gitignore for cache and logs
- Requirements specification

### Features
- **Robust Error Handling**: Handles network errors, API errors, rate limiting, and more
- **Smart Caching**: Reduces API calls and improves performance
- **Flexible Configuration**: Support for .env files and environment variables
- **Multiple Output Formats**: Markdown for humans, JSON for programs, CSV for spreadsheets
- **Rich Data Processing**: Formats pricing, architecture, and other model details
- **Advanced Filtering**: Find exactly the models you need
- **Comprehensive Statistics**: Understand the model landscape at a glance
- **Production Ready**: Includes logging, error handling, and testing support

### Technical Details
- Python 3.12+ compatible
- Uses requests library with connection pooling
- Implements retry logic with urllib3
- File-based caching with JSON
- Modular architecture for easy extension
- Type hints throughout
- Comprehensive docstrings
- Following Python best practices

### Documentation
- Complete README with installation and usage instructions
- Extensive examples document with real-world scenarios
- Inline code documentation
- Architecture overview
- Troubleshooting guide

## [Unreleased]

### Planned Features
- Unit tests with pytest
- Integration tests
- Model comparison functionality
- Historical data tracking
- Web interface option
- Additional output formats (YAML, TOML)
- Model recommendation system
- Cost calculator
- Performance benchmarks
- Multi-language support

### Possible Enhancements
- Database storage option
- API server mode
- Real-time model monitoring
- Webhook notifications
- Slack/Discord integration
- Custom model filtering DSL
- Visualization dashboard
- Export to various formats
- Integration with LangChain
- Model performance metrics

---

[1.0.0]: https://github.com/CreativeSystemsDevelopment/agent-zero/releases/tag/openrouter-v1.0.0
