# OpenRouter Model Fetcher

A fully-featured application for fetching and managing model information from OpenRouter.

## Features

- **Complete Model Information**: Fetches all available models with comprehensive details including:
  - Model names and IDs
  - Pricing information (prompt and completion tokens)
  - Context lengths
  - Model tags and capabilities
  - Full descriptions
  - Top provider information
  
- **Multiple Output Formats**: Supports Markdown, JSON, and CSV output formats

- **Advanced Analysis**: Comprehensive analysis tools for pricing, context lengths, providers, and value comparison

- **Robust Error Handling**: Comprehensive error handling and retry logic for API calls

- **Caching**: Smart caching to avoid unnecessary API calls

- **Logging**: Detailed logging for debugging and monitoring

- **Configuration Management**: Flexible configuration via environment variables or .env file

- **Demo Mode**: Test all features without an API key using sample data

## Installation

The application uses the parent project's dependencies. Ensure you have the required packages:

```bash
pip install -r ../requirements.txt
```

## Configuration

The application reads the OpenRouter API key from:
1. Environment variable `OPENROUTER_API_KEY`
2. `.env` file in the project root (one level up)

## Quick Start

### Try the Demo (No API Key Required)

Test the application without an API key:

```bash
python demo.py
# or
make demo
```

This will generate sample output files demonstrating all features.

## Usage

### Basic Usage

Fetch all models and save to Markdown (default):

```bash
python main.py
# or
make fetch
```

### Specify Output Format

```bash
# Markdown format
python main.py --format markdown

# JSON format
python main.py --format json

# CSV format
python main.py --format csv
```

### Custom Output File

```bash
python main.py --output my_models.md
```

### Enable Debug Logging

```bash
python main.py --debug
```

### Force Refresh (Bypass Cache)

```bash
python main.py --force-refresh
```

### Full Example

```bash
python main.py --format json --output models.json --debug --force-refresh
```

### Using Makefile

For convenience, use the provided Makefile:

```bash
make help           # Show available commands
make demo           # Run demo mode
make fetch          # Fetch models (Markdown)
make fetch-json     # Fetch models (JSON)
make fetch-csv      # Fetch models (CSV)
make fetch-all      # Fetch in all formats
make analyze        # Analyze models data
make clean          # Remove output files and cache
```

### Analyzing Models

After fetching models in JSON format, analyze the data:

```bash
# Full analysis
python analyze.py

# Specific analyses
python analyze.py --pricing      # Pricing analysis only
python analyze.py --context      # Context length analysis only
python analyze.py --providers    # Provider analysis only
python analyze.py --value        # Best value models only
```

## Output Files

- **Markdown** (`or_models.md`): Human-readable format with tables and sections
- **JSON** (`or_models.json`): Structured data for programmatic access
- **CSV** (`or_models.csv`): Spreadsheet-compatible format

## Architecture

### Modules

1. **`config.py`**: Configuration management and validation
2. **`api_client.py`**: OpenRouter API client with retry logic
3. **`data_processor.py`**: Data transformation and processing
4. **`formatters.py`**: Output formatters (Markdown, JSON, CSV)
5. **`cache.py`**: Caching mechanism
6. **`main.py`**: CLI interface and orchestration
7. **`demo.py`**: Demo mode with sample data
8. **`analyze.py`**: Advanced data analysis tools

### Pipeline

```
Configuration → API Client → Data Processor → Formatter → Output File
                    ↓
                  Cache
```

## Error Handling

The application includes comprehensive error handling:
- Network errors with automatic retry
- API rate limiting handling
- Invalid API key detection
- Missing configuration warnings
- Data validation errors

## Logging

Logs are written to `openrouter.log` in the same directory. Log levels:
- INFO: Normal operation
- WARNING: Non-critical issues
- ERROR: Critical errors
- DEBUG: Detailed information (use --debug flag)

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Formatters

Create a new formatter class in `formatters.py`:

```python
class NewFormatter(BaseFormatter):
    def format(self, models: List[Dict[str, Any]]) -> str:
        # Implementation
        pass
```

## License

This application is part of the Agent Zero project and follows the same license.
