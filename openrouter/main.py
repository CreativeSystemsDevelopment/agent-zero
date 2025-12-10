"""Main application for fetching OpenRouter models."""

import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

from config import Config
from api_client import OpenRouterClient, OpenRouterAPIError
from data_processor import DataProcessor
from formatters import FormatterFactory
from cache import Cache


def setup_logging(debug: bool = False) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        debug: Enable debug logging
        
    Returns:
        Configured logger
    """
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.FileHandler('openrouter.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Fetch and format OpenRouter model information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch models and save to default Markdown file
  python main.py
  
  # Fetch models and save to JSON
  python main.py --format json --output models.json
  
  # Enable debug logging
  python main.py --debug
  
  # Force refresh (bypass cache)
  python main.py --force-refresh
  
  # Filter models by tags
  python main.py --tags free opensource
  
  # Search for specific models
  python main.py --search "gpt-4"
        """
    )
    
    parser.add_argument(
        '--format',
        choices=FormatterFactory.supported_formats(),
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: or_models.<format>)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--force-refresh',
        action='store_true',
        help='Force refresh, bypass cache'
    )
    
    parser.add_argument(
        '--tags',
        nargs='+',
        help='Filter models by tags'
    )
    
    parser.add_argument(
        '--search',
        type=str,
        help='Search models by name or description'
    )
    
    parser.add_argument(
        '--min-context',
        type=int,
        help='Minimum context length'
    )
    
    return parser.parse_args()


def get_output_filename(format_type: str, custom_output: Optional[str]) -> str:
    """Determine output filename.
    
    Args:
        format_type: Output format type
        custom_output: Custom output path if provided
        
    Returns:
        Output filename
    """
    if custom_output:
        return custom_output
    
    extensions = {
        'markdown': 'md',
        'json': 'json',
        'csv': 'csv'
    }
    
    ext = extensions.get(format_type, 'txt')
    return f"or_models.{ext}"


def main():
    """Main application entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging(debug=args.debug)
    logger.info("Starting OpenRouter Model Fetcher")
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = Config()
        
        # Validate configuration
        is_valid, error_msg = config.validate()
        if not is_valid:
            logger.error(f"Configuration error: {error_msg}")
            print(f"\n❌ Configuration Error: {error_msg}\n")
            sys.exit(1)
        
        logger.info("Configuration validated successfully")
        logger.debug(f"Config: {config}")
        
        # Setup cache
        cache_dir = Path(__file__).parent / ".cache"
        cache = Cache(cache_dir, ttl_seconds=config.cache_ttl)
        
        # Fetch models
        models = None
        
        if not args.force_refresh:
            logger.info("Checking cache...")
            models = cache.get()
        
        if models is None:
            logger.info("Fetching models from API...")
            with OpenRouterClient(config) as client:
                models = client.fetch_models()
            
            # Cache the results
            cache.set(models)
        else:
            logger.info(f"Using cached data ({len(models)} models)")
        
        # Process models
        logger.info("Processing model data...")
        processor = DataProcessor()
        processed_models = processor.process_models(models)
        
        # Apply filters if specified
        if args.tags or args.search or args.min_context:
            logger.info("Applying filters...")
            filtered_count = len(processed_models)
            
            processed_models = processor.filter_models(
                processed_models,
                tags=args.tags,
                search=args.search,
                min_context=args.min_context
            )
            
            logger.info(f"Filtered from {filtered_count} to {len(processed_models)} models")
        
        # Calculate statistics
        logger.info("Calculating statistics...")
        stats = processor.get_statistics(processed_models)
        
        # Format output
        logger.info(f"Formatting output as {args.format}...")
        formatter = FormatterFactory.create(args.format)
        formatted_output = formatter.format(processed_models, stats)
        
        # Write to file
        output_file = get_output_filename(args.format, args.output)
        output_path = Path(__file__).parent / output_file
        
        logger.info(f"Writing output to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        
        # Success message
        print(f"\n✅ Successfully fetched and saved {len(processed_models)} models")
        print(f"📄 Output file: {output_path}")
        print(f"📊 Statistics:")
        print(f"   - Total models: {stats['total_models']}")
        print(f"   - Unique tags: {stats['unique_tags']}")
        print(f"   - Average context: {stats['average_context_length']:,} tokens")
        print(f"   - Max context: {stats['max_context_length']:,} tokens")
        print()
        
        logger.info("Application completed successfully")
        
    except OpenRouterAPIError as e:
        logger.error(f"API Error: {e}")
        print(f"\n❌ API Error: {e}\n")
        sys.exit(1)
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected Error: {e}\n")
        print("Check openrouter.log for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
