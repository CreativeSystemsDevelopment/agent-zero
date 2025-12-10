# OpenRouter Model Fetcher - Usage Examples

This document provides comprehensive examples of how to use the OpenRouter Model Fetcher.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Output Formats](#output-formats)
- [Filtering Models](#filtering-models)
- [Advanced Usage](#advanced-usage)
- [Integration Examples](#integration-examples)
- [Troubleshooting](#troubleshooting)

## Basic Usage

### Fetch All Models (Default Markdown)

The simplest way to fetch all models:

```bash
python main.py
```

This will:
- Fetch all available models from OpenRouter
- Process and format the data
- Save to `or_models.md` in the current directory
- Use cached data if available and not expired

### With Debug Logging

Enable detailed logging to see what's happening:

```bash
python main.py --debug
```

Debug logs are written to `openrouter.log` and displayed in console.

## Output Formats

### Markdown Format (Default)

Creates a comprehensive, human-readable document:

```bash
python main.py --format markdown
```

Features:
- Statistics overview
- Models table with key information
- Detailed section for each model
- Well-formatted with headers and sections

### JSON Format

For programmatic access and integration:

```bash
python main.py --format json --output models.json
```

Features:
- Complete model data structure
- Metadata with timestamp and statistics
- Easy to parse and integrate with other tools

### CSV Format

For spreadsheet applications:

```bash
python main.py --format csv --output models.csv
```

Features:
- Rows and columns for easy filtering
- Compatible with Excel, Google Sheets, etc.
- Good for data analysis

## Filtering Models

### Filter by Tags

Find models with specific tags:

```bash
# Find all free models
python main.py --tags free

# Find models with multiple tags (OR logic)
python main.py --tags free opensource

# Save filtered results
python main.py --tags free --output free_models.md
```

### Search by Name or Description

Search for specific models:

```bash
# Search for GPT models
python main.py --search "gpt"

# Search for Claude models
python main.py --search "claude"

# Search for Llama models
python main.py --search "llama"
```

### Filter by Context Length

Find models with minimum context length:

```bash
# Models with at least 32K context
python main.py --min-context 32000

# Models with at least 128K context
python main.py --min-context 128000
```

### Combine Multiple Filters

All filters can be combined:

```bash
# Find free models with GPT in name and at least 8K context
python main.py --tags free --search "gpt" --min-context 8000 --output filtered.md
```

## Advanced Usage

### Force Refresh (Bypass Cache)

Fetch fresh data from API:

```bash
python main.py --force-refresh
```

Use when:
- You need the latest model information
- Cache might be corrupted
- New models have been added

### Custom Output Path

Specify exact output location:

```bash
# Save to specific directory
python main.py --output /path/to/output/models.md

# Save with custom name
python main.py --output my_custom_models.json --format json
```

### Quiet Mode with Only Errors

Redirect stdout to suppress normal output:

```bash
python main.py > /dev/null 2>&1
```

Check `openrouter.log` for results.

## Integration Examples

### Use in Shell Scripts

```bash
#!/bin/bash

# Fetch models
python main.py --format json --output models.json

# Check if successful
if [ $? -eq 0 ]; then
    echo "✅ Models fetched successfully"
    # Process the JSON with jq or other tools
    cat models.json | jq '.models[0]'
else
    echo "❌ Failed to fetch models"
    exit 1
fi
```

### Scheduled Updates with Cron

Add to crontab to fetch models daily:

```cron
# Fetch models every day at 2 AM
0 2 * * * cd /path/to/openrouter && python main.py --force-refresh
```

### Python Integration

```python
import json
import subprocess

# Run the fetcher
result = subprocess.run(
    ['python', 'main.py', '--format', 'json', '--output', 'models.json'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    # Load and use the data
    with open('models.json', 'r') as f:
        data = json.load(f)
    
    models = data['models']
    print(f"Found {len(models)} models")
    
    # Find specific model
    gpt4_models = [m for m in models if 'gpt-4' in m['id'].lower()]
    print(f"Found {len(gpt4_models)} GPT-4 models")
else:
    print(f"Error: {result.stderr}")
```

### Use with Make

```makefile
.PHONY: fetch-models fetch-free fetch-all

fetch-models:
	@echo "Fetching OpenRouter models..."
	python main.py

fetch-free:
	@echo "Fetching free models..."
	python main.py --tags free --output free_models.md

fetch-all:
	@echo "Fetching all formats..."
	python main.py --format markdown --force-refresh
	python main.py --format json --output models.json
	python main.py --format csv --output models.csv
```

## Workflow Examples

### Daily Model Updates

```bash
#!/bin/bash
# daily_update.sh

OPENROUTER_DIR="/path/to/openrouter"
cd "$OPENROUTER_DIR"

# Fetch fresh data
python main.py --force-refresh --format json --output models.json

# Create different filtered views
python main.py --tags free --output free_models.md
python main.py --min-context 100000 --output long_context_models.md
python main.py --search "gpt" --output gpt_models.md

# Notify completion
echo "✅ Daily model update completed at $(date)"
```

### Compare Models

```bash
# Fetch current models
python main.py --format json --output models_today.json

# Later, fetch again
python main.py --format json --output models_later.json

# Compare (using jq or custom script)
diff <(jq '.models[].id' models_today.json | sort) \
     <(jq '.models[].id' models_later.json | sort)
```

## Troubleshooting

### API Key Issues

If you see "API key not found":

```bash
# Check if API key is set
echo $OPENROUTER_API_KEY

# Set it temporarily
export OPENROUTER_API_KEY="your-key-here"
python main.py

# Or add to .env file in project root
echo "OPENROUTER_API_KEY=your-key-here" >> ../.env
```

### Network Errors

If you encounter network issues:

```bash
# Enable debug logging to see details
python main.py --debug

# Check your internet connection
ping openrouter.ai

# Try with longer timeout (modify config.py if needed)
```

### Cache Issues

If cached data seems stale:

```bash
# Force refresh
python main.py --force-refresh

# Or manually clear cache
rm -rf .cache/
```

### Permission Issues

If you can't write output file:

```bash
# Check permissions
ls -la

# Use a different output location
python main.py --output ~/models.md

# Or fix permissions
chmod +w .
```

## Best Practices

1. **Use caching** for frequent queries to avoid rate limits
2. **Force refresh** periodically (e.g., daily) to get latest data
3. **Use filters** to create specific model lists for different use cases
4. **Keep logs** by using `--debug` when troubleshooting
5. **Validate output** by checking the generated files
6. **Monitor API usage** to stay within rate limits
7. **Backup important outputs** before regenerating

## Getting Help

- Check `openrouter.log` for detailed error messages
- Use `--debug` flag for verbose output
- Read the main README.md for architecture details
- Review the code in `main.py` for customization options
