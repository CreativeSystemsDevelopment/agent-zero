.PHONY: help demo fetch fetch-json fetch-csv fetch-all analyze clean install test

help:
	@echo "OpenRouter Model Fetcher - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "  make demo          - Run demo mode with sample data"
	@echo "  make fetch         - Fetch models (Markdown format)"
	@echo "  make fetch-json    - Fetch models (JSON format)"
	@echo "  make fetch-csv     - Fetch models (CSV format)"
	@echo "  make fetch-all     - Fetch models in all formats"
	@echo "  make analyze       - Analyze models from JSON file"
	@echo "  make clean         - Remove output files and cache"
	@echo "  make install       - Install required dependencies"
	@echo "  make test          - Run tests (if available)"
	@echo ""

demo:
	@echo "Running demo mode..."
	python demo.py

fetch:
	@echo "Fetching models in Markdown format..."
	python main.py --format markdown

fetch-json:
	@echo "Fetching models in JSON format..."
	python main.py --format json --output or_models.json

fetch-csv:
	@echo "Fetching models in CSV format..."
	python main.py --format csv --output or_models.csv

fetch-all:
	@echo "Fetching models in all formats..."
	@python main.py --format markdown --force-refresh
	@python main.py --format json --output or_models.json
	@python main.py --format csv --output or_models.csv
	@echo ""
	@echo "✅ All formats generated:"
	@ls -lh or_models.*

analyze:
	@echo "Analyzing models data..."
	@if [ -f "or_models.json" ]; then \
		python analyze.py; \
	else \
		echo "❌ or_models.json not found. Run 'make fetch-json' first."; \
		exit 1; \
	fi

clean:
	@echo "Cleaning up..."
	@rm -f or_models.* demo_models.* *.log
	@rm -rf .cache/ __pycache__/
	@echo "✅ Cleanup complete"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

test:
	@echo "Running tests..."
	@if [ -f "test_*.py" ]; then \
		python -m pytest -v; \
	else \
		echo "No tests found. Run 'make demo' to verify functionality."; \
	fi
