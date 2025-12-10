"""Data processing and transformation for model information."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class DataProcessor:
    """Processor for transforming and enriching model data."""
    
    @staticmethod
    def process_models(models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and enrich model data.
        
        Args:
            models: Raw model data from API
            
        Returns:
            Processed model data
        """
        processed = []
        
        for model in models:
            try:
                processed_model = DataProcessor._process_single_model(model)
                processed.append(processed_model)
            except Exception as e:
                logger.error(f"Error processing model {model.get('id', 'unknown')}: {e}")
                # Include the model even if processing partially fails
                processed.append(model)
        
        # Sort by model ID for consistent output
        processed.sort(key=lambda m: m.get("id", ""))
        
        logger.info(f"Processed {len(processed)} models")
        return processed
    
    @staticmethod
    def _process_single_model(model: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single model entry.
        
        Args:
            model: Raw model data
            
        Returns:
            Processed model data
        """
        processed = model.copy()
        
        # Extract and format pricing information
        pricing = model.get("pricing", {})
        processed["pricing_formatted"] = DataProcessor._format_pricing(pricing)
        
        # Extract context length
        processed["context_length"] = model.get("context_length", "Unknown")
        
        # Extract and format architecture
        architecture = model.get("architecture", {})
        processed["architecture_summary"] = DataProcessor._format_architecture(architecture)
        
        # Extract top provider
        top_provider = model.get("top_provider", {})
        processed["top_provider_name"] = top_provider.get("name", "Unknown")
        processed["top_provider_context"] = top_provider.get("context_length", "Unknown")
        
        # Extract model name and description
        processed["name"] = model.get("name", model.get("id", "Unknown"))
        processed["description"] = model.get("description", "No description available")
        
        # Extract created timestamp
        created = model.get("created")
        if created:
            try:
                dt = datetime.fromtimestamp(created)
                processed["created_formatted"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                processed["created_formatted"] = "Unknown"
        else:
            processed["created_formatted"] = "Unknown"
        
        return processed
    
    @staticmethod
    def _format_pricing(pricing: Dict[str, Any]) -> str:
        """Format pricing information.
        
        Args:
            pricing: Pricing dictionary
            
        Returns:
            Formatted pricing string
        """
        if not pricing:
            return "Pricing not available"
        
        prompt = pricing.get("prompt", "N/A")
        completion = pricing.get("completion", "N/A")
        
        # Convert to more readable format (from dollars to dollars per million tokens)
        try:
            if prompt != "N/A":
                prompt_val = float(prompt) * 1_000_000
                prompt = f"${prompt_val:.2f}/1M"
            if completion != "N/A":
                completion_val = float(completion) * 1_000_000
                completion = f"${completion_val:.2f}/1M"
        except (ValueError, TypeError):
            pass
        
        return f"Prompt: {prompt}, Completion: {completion}"
    
    @staticmethod
    def _format_architecture(architecture: Dict[str, Any]) -> str:
        """Format architecture information.
        
        Args:
            architecture: Architecture dictionary
            
        Returns:
            Formatted architecture string
        """
        if not architecture:
            return "Unknown architecture"
        
        modality = architecture.get("modality", "Unknown")
        tokenizer = architecture.get("tokenizer", "Unknown")
        instruct_type = architecture.get("instruct_type", "Unknown")
        
        return f"Modality: {modality}, Tokenizer: {tokenizer}, Type: {instruct_type}"
    
    @staticmethod
    def filter_models(
        models: List[Dict[str, Any]],
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        min_context: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Filter models based on criteria.
        
        Args:
            models: List of models to filter
            tags: Filter by tags (any match)
            search: Search string for name/description
            min_context: Minimum context length
            
        Returns:
            Filtered list of models
        """
        filtered = models
        
        if tags:
            filtered = [
                m for m in filtered
                if any(tag in m.get("tags", []) for tag in tags)
            ]
        
        if search:
            search_lower = search.lower()
            filtered = [
                m for m in filtered
                if search_lower in m.get("name", "").lower()
                or search_lower in m.get("description", "").lower()
                or search_lower in m.get("id", "").lower()
            ]
        
        if min_context:
            filtered = [
                m for m in filtered
                if isinstance(m.get("context_length"), int)
                and m["context_length"] >= min_context
            ]
        
        return filtered
    
    @staticmethod
    def get_statistics(models: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics about the models.
        
        Args:
            models: List of models
            
        Returns:
            Statistics dictionary
        """
        total = len(models)
        
        # Count by modality
        modalities = {}
        for model in models:
            arch = model.get("architecture", {})
            modality = arch.get("modality", "Unknown")
            modalities[modality] = modalities.get(modality, 0) + 1
        
        # Count unique tags
        all_tags = set()
        for model in models:
            tags = model.get("tags", [])
            all_tags.update(tags)
        
        # Calculate average context length
        context_lengths = [
            m.get("context_length", 0)
            for m in models
            if isinstance(m.get("context_length"), int)
        ]
        avg_context = sum(context_lengths) / len(context_lengths) if context_lengths else 0
        max_context = max(context_lengths) if context_lengths else 0
        
        return {
            "total_models": total,
            "modalities": modalities,
            "unique_tags": len(all_tags),
            "tags": sorted(list(all_tags)),
            "average_context_length": int(avg_context),
            "max_context_length": max_context
        }
