"""Analyze OpenRouter models data from JSON output."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_models(filepath: str = "or_models.json") -> Dict[str, Any]:
    """Load models from JSON file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Models data dictionary
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        print("Run 'python main.py --format json' first to generate the file.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON file: {e}")
        sys.exit(1)


def analyze_pricing(models: List[Dict[str, Any]]):
    """Analyze pricing across models."""
    print("\n" + "=" * 70)
    print("PRICING ANALYSIS")
    print("=" * 70)
    
    pricing_data = []
    for model in models:
        pricing = model.get("pricing", {})
        if pricing:
            try:
                prompt = float(pricing.get("prompt", 0))
                completion = float(pricing.get("completion", 0))
                avg_price = (prompt + completion) / 2
                pricing_data.append({
                    "model": model.get("name", "Unknown"),
                    "id": model.get("id", "Unknown"),
                    "prompt": prompt * 1_000_000,
                    "completion": completion * 1_000_000,
                    "average": avg_price * 1_000_000
                })
            except (ValueError, TypeError):
                pass
    
    if not pricing_data:
        print("No pricing data available")
        return
    
    # Sort by average price
    pricing_data.sort(key=lambda x: x["average"])
    
    print("\nMost Affordable Models (by average price per 1M tokens):")
    for i, model in enumerate(pricing_data[:10], 1):
        print(f"{i:2d}. {model['model']:<40} ${model['average']:.2f}")
    
    print("\nMost Expensive Models (by average price per 1M tokens):")
    for i, model in enumerate(reversed(pricing_data[-10:]), 1):
        print(f"{i:2d}. {model['model']:<40} ${model['average']:.2f}")
    
    # Calculate statistics
    avg_prompt = sum(m["prompt"] for m in pricing_data) / len(pricing_data)
    avg_completion = sum(m["completion"] for m in pricing_data) / len(pricing_data)
    
    print(f"\nPricing Statistics:")
    print(f"  Average Prompt Price: ${avg_prompt:.2f}/1M tokens")
    print(f"  Average Completion Price: ${avg_completion:.2f}/1M tokens")


def analyze_context_lengths(models: List[Dict[str, Any]]):
    """Analyze context lengths across models."""
    print("\n" + "=" * 70)
    print("CONTEXT LENGTH ANALYSIS")
    print("=" * 70)
    
    context_data = []
    for model in models:
        context = model.get("context_length")
        if isinstance(context, int):
            context_data.append({
                "model": model.get("name", "Unknown"),
                "id": model.get("id", "Unknown"),
                "context": context
            })
    
    if not context_data:
        print("No context length data available")
        return
    
    # Sort by context length
    context_data.sort(key=lambda x: x["context"], reverse=True)
    
    print("\nLargest Context Windows:")
    for i, model in enumerate(context_data[:10], 1):
        print(f"{i:2d}. {model['model']:<40} {model['context']:>10,} tokens")
    
    # Group by ranges
    ranges = {
        "< 8K": 0,
        "8K - 32K": 0,
        "32K - 128K": 0,
        "128K - 1M": 0,
        "> 1M": 0
    }
    
    for model in context_data:
        ctx = model["context"]
        if ctx < 8000:
            ranges["< 8K"] += 1
        elif ctx < 32000:
            ranges["8K - 32K"] += 1
        elif ctx < 128000:
            ranges["32K - 128K"] += 1
        elif ctx < 1000000:
            ranges["128K - 1M"] += 1
        else:
            ranges["> 1M"] += 1
    
    print("\nModels by Context Length Range:")
    for range_name, count in ranges.items():
        percentage = (count / len(context_data)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {range_name:<15} {count:3d} models ({percentage:5.1f}%) {bar}")


def analyze_providers(models: List[Dict[str, Any]]):
    """Analyze top providers."""
    print("\n" + "=" * 70)
    print("PROVIDER ANALYSIS")
    print("=" * 70)
    
    providers = defaultdict(int)
    for model in models:
        provider = model.get("top_provider_name", "Unknown")
        providers[provider] += 1
    
    # Sort by count
    sorted_providers = sorted(providers.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTop Providers by Model Count:")
    for i, (provider, count) in enumerate(sorted_providers[:15], 1):
        percentage = (count / len(models)) * 100
        bar = "█" * int(percentage)
        print(f"{i:2d}. {provider:<30} {count:3d} models ({percentage:5.1f}%) {bar}")


def analyze_modalities(models: List[Dict[str, Any]]):
    """Analyze model modalities."""
    print("\n" + "=" * 70)
    print("MODALITY ANALYSIS")
    print("=" * 70)
    
    modalities = defaultdict(int)
    for model in models:
        arch = model.get("architecture", {})
        modality = arch.get("modality", "Unknown")
        modalities[modality] += 1
    
    print("\nModels by Modality:")
    for modality, count in sorted(modalities.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(models)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {modality:<20} {count:3d} models ({percentage:5.1f}%) {bar}")


def analyze_tags(models: List[Dict[str, Any]]):
    """Analyze model tags."""
    print("\n" + "=" * 70)
    print("TAG ANALYSIS")
    print("=" * 70)
    
    tag_counts = defaultdict(int)
    for model in models:
        tags = model.get("tags", [])
        for tag in tags:
            tag_counts[tag] += 1
    
    # Sort by count
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("\nMost Common Tags:")
    for i, (tag, count) in enumerate(sorted_tags[:20], 1):
        percentage = (count / len(models)) * 100
        bar = "█" * int(percentage)
        print(f"{i:2d}. {tag:<25} {count:3d} models ({percentage:5.1f}%) {bar}")


def find_best_value_models(models: List[Dict[str, Any]]):
    """Find models with best value (context per dollar)."""
    print("\n" + "=" * 70)
    print("BEST VALUE MODELS (Context per Dollar)")
    print("=" * 70)
    
    value_models = []
    for model in models:
        context = model.get("context_length")
        pricing = model.get("pricing", {})
        
        if isinstance(context, int) and pricing:
            try:
                prompt = float(pricing.get("prompt", 0))
                completion = float(pricing.get("completion", 0))
                avg_price = (prompt + completion) / 2
                
                if avg_price > 0:
                    value = context / (avg_price * 1_000_000)
                    value_models.append({
                        "model": model.get("name", "Unknown"),
                        "id": model.get("id", "Unknown"),
                        "value": value,
                        "context": context,
                        "price": avg_price * 1_000_000
                    })
            except (ValueError, TypeError):
                pass
    
    if not value_models:
        print("Insufficient data for value analysis")
        return
    
    # Sort by value
    value_models.sort(key=lambda x: x["value"], reverse=True)
    
    print("\nTop 10 Best Value Models:")
    print(f"{'Rank':<6} {'Model':<35} {'Context':<12} {'Price/1M':<12} {'Value':<10}")
    print("-" * 85)
    for i, model in enumerate(value_models[:10], 1):
        print(f"{i:<6} {model['model']:<35} {model['context']:>10,} ${model['price']:>9.2f} {model['value']:>10.0f}")


def main():
    """Main analysis function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze OpenRouter models data")
    parser.add_argument(
        "--file",
        default="or_models.json",
        help="JSON file to analyze (default: or_models.json)"
    )
    parser.add_argument(
        "--pricing",
        action="store_true",
        help="Show only pricing analysis"
    )
    parser.add_argument(
        "--context",
        action="store_true",
        help="Show only context length analysis"
    )
    parser.add_argument(
        "--providers",
        action="store_true",
        help="Show only provider analysis"
    )
    parser.add_argument(
        "--modalities",
        action="store_true",
        help="Show only modality analysis"
    )
    parser.add_argument(
        "--tags",
        action="store_true",
        help="Show only tag analysis"
    )
    parser.add_argument(
        "--value",
        action="store_true",
        help="Show only best value models"
    )
    
    args = parser.parse_args()
    
    # Load data
    data = load_models(args.file)
    models = data.get("models", [])
    metadata = data.get("metadata", {})
    
    print("=" * 70)
    print("OPENROUTER MODELS ANALYSIS")
    print("=" * 70)
    print(f"\nTotal Models: {len(models)}")
    if metadata.get("timestamp"):
        print(f"Data Timestamp: {metadata['timestamp']}")
    
    # If no specific analysis requested, show all
    show_all = not any([
        args.pricing, args.context, args.providers,
        args.modalities, args.tags, args.value
    ])
    
    if show_all or args.pricing:
        analyze_pricing(models)
    
    if show_all or args.context:
        analyze_context_lengths(models)
    
    if show_all or args.providers:
        analyze_providers(models)
    
    if show_all or args.modalities:
        analyze_modalities(models)
    
    if show_all or args.tags:
        analyze_tags(models)
    
    if show_all or args.value:
        find_best_value_models(models)
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
