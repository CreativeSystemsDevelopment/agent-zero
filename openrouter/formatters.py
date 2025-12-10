"""Output formatters for model data."""

import json
import csv
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from io import StringIO
from datetime import datetime


class BaseFormatter(ABC):
    """Base class for output formatters."""
    
    @abstractmethod
    def format(self, models: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """Format model data.
        
        Args:
            models: List of processed models
            stats: Statistics about the models
            
        Returns:
            Formatted string
        """
        pass


class MarkdownFormatter(BaseFormatter):
    """Formatter for Markdown output."""
    
    def format(self, models: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """Format models as Markdown.
        
        Args:
            models: List of processed models
            stats: Statistics about the models
            
        Returns:
            Markdown formatted string
        """
        output = []
        
        # Header
        output.append("# OpenRouter Models")
        output.append("")
        output.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        output.append("")
        
        # Statistics
        output.append("## Statistics")
        output.append("")
        output.append(f"- **Total Models**: {stats['total_models']}")
        output.append(f"- **Unique Tags**: {stats['unique_tags']}")
        output.append(f"- **Average Context Length**: {stats['average_context_length']:,} tokens")
        output.append(f"- **Max Context Length**: {stats['max_context_length']:,} tokens")
        output.append("")
        
        # Modalities breakdown
        if stats['modalities']:
            output.append("### Models by Modality")
            output.append("")
            for modality, count in sorted(stats['modalities'].items(), key=lambda x: x[1], reverse=True):
                output.append(f"- **{modality}**: {count} models")
            output.append("")
        
        # All tags
        if stats['tags']:
            output.append("### Available Tags")
            output.append("")
            output.append(", ".join(f"`{tag}`" for tag in stats['tags']))
            output.append("")
        
        # Models table
        output.append("## Models")
        output.append("")
        output.append("| Model ID | Name | Context | Pricing | Top Provider |")
        output.append("|----------|------|---------|---------|--------------|")
        
        for model in models:
            model_id = model.get("id", "N/A")
            name = model.get("name", "N/A")
            context = model.get("context_length", "N/A")
            if isinstance(context, int):
                context = f"{context:,}"
            pricing = model.get("pricing_formatted", "N/A")
            provider = model.get("top_provider_name", "N/A")
            
            # Escape pipe characters in table cells
            name = str(name).replace("|", "\\|")
            pricing = str(pricing).replace("|", "\\|")
            provider = str(provider).replace("|", "\\|")
            
            output.append(f"| `{model_id}` | {name} | {context} | {pricing} | {provider} |")
        
        output.append("")
        
        # Detailed model information
        output.append("## Detailed Model Information")
        output.append("")
        
        for model in models:
            model_id = model.get("id", "N/A")
            name = model.get("name", "N/A")
            description = model.get("description", "No description available")
            context = model.get("context_length", "N/A")
            if isinstance(context, int):
                context = f"{context:,}"
            pricing = model.get("pricing_formatted", "N/A")
            architecture = model.get("architecture_summary", "Unknown")
            provider = model.get("top_provider_name", "N/A")
            provider_context = model.get("top_provider_context", "N/A")
            if isinstance(provider_context, int):
                provider_context = f"{provider_context:,}"
            created = model.get("created_formatted", "Unknown")
            tags = model.get("tags", [])
            
            output.append(f"### {name}")
            output.append("")
            output.append(f"**Model ID**: `{model_id}`")
            output.append("")
            output.append(f"**Description**: {description}")
            output.append("")
            output.append(f"**Context Length**: {context} tokens")
            output.append("")
            output.append(f"**Pricing**: {pricing}")
            output.append("")
            output.append(f"**Architecture**: {architecture}")
            output.append("")
            output.append(f"**Top Provider**: {provider} (Context: {provider_context})")
            output.append("")
            output.append(f"**Created**: {created}")
            output.append("")
            
            if tags:
                output.append(f"**Tags**: {', '.join(f'`{tag}`' for tag in tags)}")
                output.append("")
            
            output.append("---")
            output.append("")
        
        return "\n".join(output)


class JSONFormatter(BaseFormatter):
    """Formatter for JSON output."""
    
    def format(self, models: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """Format models as JSON.
        
        Args:
            models: List of processed models
            stats: Statistics about the models
            
        Returns:
            JSON formatted string
        """
        output = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_models": len(models),
                "statistics": stats
            },
            "models": models
        }
        
        return json.dumps(output, indent=2, ensure_ascii=False)


class CSVFormatter(BaseFormatter):
    """Formatter for CSV output."""
    
    def format(self, models: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """Format models as CSV.
        
        Args:
            models: List of processed models
            stats: Statistics about the models
            
        Returns:
            CSV formatted string
        """
        if not models:
            return ""
        
        output = StringIO()
        
        # Define CSV columns
        fieldnames = [
            "id",
            "name",
            "description",
            "context_length",
            "pricing_formatted",
            "architecture_summary",
            "top_provider_name",
            "top_provider_context",
            "created_formatted",
            "tags"
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for model in models:
            # Convert tags list to string
            row = model.copy()
            if "tags" in row and isinstance(row["tags"], list):
                row["tags"] = ", ".join(row["tags"])
            
            writer.writerow(row)
        
        return output.getvalue()


class FormatterFactory:
    """Factory for creating formatters."""
    
    _formatters = {
        "markdown": MarkdownFormatter,
        "json": JSONFormatter,
        "csv": CSVFormatter
    }
    
    @classmethod
    def create(cls, format_type: str) -> BaseFormatter:
        """Create a formatter instance.
        
        Args:
            format_type: Type of formatter (markdown, json, csv)
            
        Returns:
            Formatter instance
            
        Raises:
            ValueError: If format type is not supported
        """
        formatter_class = cls._formatters.get(format_type.lower())
        
        if not formatter_class:
            supported = ", ".join(cls._formatters.keys())
            raise ValueError(
                f"Unsupported format: {format_type}. "
                f"Supported formats: {supported}"
            )
        
        return formatter_class()
    
    @classmethod
    def supported_formats(cls) -> List[str]:
        """Get list of supported formats.
        
        Returns:
            List of format names
        """
        return list(cls._formatters.keys())
