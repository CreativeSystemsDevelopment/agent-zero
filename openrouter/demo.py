"""Demo mode for testing the application without API access."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from data_processor import DataProcessor
from formatters import FormatterFactory


def generate_sample_data() -> List[Dict[str, Any]]:
    """Generate sample model data for demonstration.
    
    Returns:
        List of sample model dictionaries
    """
    return [
        {
            "id": "openai/gpt-4-turbo",
            "name": "GPT-4 Turbo",
            "description": "The latest GPT-4 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Maximum of 4096 output tokens.",
            "context_length": 128000,
            "pricing": {
                "prompt": "0.00001",
                "completion": "0.00003"
            },
            "top_provider": {
                "name": "OpenAI",
                "context_length": 128000
            },
            "architecture": {
                "modality": "text",
                "tokenizer": "GPT",
                "instruct_type": "chat"
            },
            "tags": ["featured", "chat", "functions"],
            "created": 1699564800
        },
        {
            "id": "anthropic/claude-3-opus",
            "name": "Claude 3 Opus",
            "description": "Anthropic's most powerful model, offering best-in-class performance on highly complex tasks. Excels at research, advanced math, coding, and extended instruction following.",
            "context_length": 200000,
            "pricing": {
                "prompt": "0.000015",
                "completion": "0.000075"
            },
            "top_provider": {
                "name": "Anthropic",
                "context_length": 200000
            },
            "architecture": {
                "modality": "text",
                "tokenizer": "Claude",
                "instruct_type": "chat"
            },
            "tags": ["featured", "chat", "extended-context"],
            "created": 1709510400
        },
        {
            "id": "meta-llama/llama-3-70b-instruct",
            "name": "Llama 3 70B Instruct",
            "description": "Meta's latest open-source large language model with 70 billion parameters. Optimized for instruction following and dialogue applications.",
            "context_length": 8192,
            "pricing": {
                "prompt": "0.0000009",
                "completion": "0.0000009"
            },
            "top_provider": {
                "name": "Together AI",
                "context_length": 8192
            },
            "architecture": {
                "modality": "text",
                "tokenizer": "Llama",
                "instruct_type": "instruct"
            },
            "tags": ["opensource", "chat", "free"],
            "created": 1713398400
        },
        {
            "id": "mistralai/mixtral-8x7b-instruct",
            "name": "Mixtral 8x7B Instruct",
            "description": "A high-quality sparse mixture of experts model with 8 experts of 7B parameters each. Offers excellent performance with efficient compute usage.",
            "context_length": 32768,
            "pricing": {
                "prompt": "0.00000027",
                "completion": "0.00000027"
            },
            "top_provider": {
                "name": "Mistral AI",
                "context_length": 32768
            },
            "architecture": {
                "modality": "text",
                "tokenizer": "Mistral",
                "instruct_type": "instruct"
            },
            "tags": ["opensource", "chat", "moe"],
            "created": 1702339200
        },
        {
            "id": "google/gemini-pro-1.5",
            "name": "Gemini Pro 1.5",
            "description": "Google's most capable multimodal model with a 1 million token context window. Excels at understanding and reasoning across text, images, video, and audio.",
            "context_length": 1000000,
            "pricing": {
                "prompt": "0.00000125",
                "completion": "0.000005"
            },
            "top_provider": {
                "name": "Google",
                "context_length": 1000000
            },
            "architecture": {
                "modality": "multimodal",
                "tokenizer": "Gemini",
                "instruct_type": "chat"
            },
            "tags": ["featured", "chat", "multimodal", "extended-context"],
            "created": 1707868800
        }
    ]


def run_demo():
    """Run the demonstration."""
    print("=" * 70)
    print("OpenRouter Model Fetcher - DEMO MODE")
    print("=" * 70)
    print()
    print("This demo uses sample data to demonstrate the application features")
    print("without requiring an API key.")
    print()
    
    # Generate sample data
    print("📊 Generating sample model data...")
    models = generate_sample_data()
    print(f"✅ Generated {len(models)} sample models")
    print()
    
    # Process models
    print("⚙️  Processing model data...")
    processor = DataProcessor()
    processed_models = processor.process_models(models)
    print(f"✅ Processed {len(processed_models)} models")
    print()
    
    # Calculate statistics
    print("📈 Calculating statistics...")
    stats = processor.get_statistics(processed_models)
    print(f"✅ Statistics calculated")
    print(f"   - Total models: {stats['total_models']}")
    print(f"   - Unique tags: {stats['unique_tags']}")
    print(f"   - Tags: {', '.join(stats['tags'])}")
    print(f"   - Average context: {stats['average_context_length']:,} tokens")
    print(f"   - Max context: {stats['max_context_length']:,} tokens")
    print()
    
    # Generate outputs in all formats
    output_dir = Path(__file__).parent
    
    formats = ['markdown', 'json', 'csv']
    print("📝 Generating output files...")
    
    for format_type in formats:
        formatter = FormatterFactory.create(format_type)
        output = formatter.format(processed_models, stats)
        
        filename = f"demo_models.{format_type if format_type != 'markdown' else 'md'}"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"   ✅ {filename} ({len(output)} bytes)")
    
    print()
    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70)
    print()
    print("Generated files:")
    print("  - demo_models.md   (Markdown format)")
    print("  - demo_models.json (JSON format)")
    print("  - demo_models.csv  (CSV format)")
    print()
    print("To use with real API:")
    print("  1. Get an API key from https://openrouter.ai/keys")
    print("  2. Add OPENROUTER_API_KEY to ../.env file")
    print("  3. Run: python main.py")
    print()
    
    # Test filtering
    print("🔍 Testing filtering capabilities...")
    print()
    
    # Filter by tags
    free_models = processor.filter_models(processed_models, tags=['free'])
    print(f"   📌 Free models: {len(free_models)}")
    for model in free_models:
        print(f"      - {model['name']}")
    print()
    
    # Filter by search
    gpt_models = processor.filter_models(processed_models, search='gpt')
    print(f"   🔎 Models matching 'gpt': {len(gpt_models)}")
    for model in gpt_models:
        print(f"      - {model['name']}")
    print()
    
    # Filter by context
    long_context = processor.filter_models(processed_models, min_context=100000)
    print(f"   📏 Models with 100K+ context: {len(long_context)}")
    for model in long_context:
        print(f"      - {model['name']} ({model['context_length']:,} tokens)")
    print()


if __name__ == "__main__":
    run_demo()
