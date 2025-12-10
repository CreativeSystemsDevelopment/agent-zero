#!/bin/bash
# Convenience script to run the OpenRouter Model Fetcher

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Run the application with all passed arguments
python main.py "$@"
