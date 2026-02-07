#!/usr/bin/env python3
"""
Generate random Kung Fu Panda quotes by theme
This script creates theme-specific API endpoint files for TRMNL
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path


def load_quotes():
    """Load all quotes from quotes.json"""
    quotes_file = Path(__file__).parent / "quotes.json"
    
    if not quotes_file.exists():
        return [{
            "error": "quotes.json not found",
            "text": "There are no accidents...",
            "author": "Master Oogway",
            "movie": "Kung Fu Panda",
            "theme": "Wisdom"
        }]
    
    with open(quotes_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_random_quote(theme_filter=None):
    """Generate a random quote, optionally filtered by theme
    
    Args:
        theme_filter: Theme to filter by (e.g., 'wisdom', 'humor'), or None for all quotes
    
    Returns:
        Dictionary containing quote data with timestamp
    """
    all_quotes = load_quotes()
    
    # Filter by theme if specified
    if theme_filter and theme_filter.lower() != 'all':
        filtered_quotes = [q for q in all_quotes if q.get('theme', '').lower() == theme_filter.lower()]
        if not filtered_quotes:
            print(f"⚠️  No quotes found for theme '{theme_filter}', using all quotes")
            filtered_quotes = all_quotes
        quotes = filtered_quotes
    else:
        quotes = all_quotes
    
    quote = random.choice(quotes)
    
    # Add timestamp
    quote['updated_on'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    return quote


def save_random_quote(theme=None, output_file=None):
    """Generate quote and save to API endpoint
    
    Args:
        theme: Theme to filter by (e.g., 'wisdom', 'humor', 'all')
        output_file: Custom output path (auto-generated if None)
    
    Returns:
        The generated quote dictionary
    """
    # Use theme-specific filename if not provided
    if output_file is None:
        theme_suffix = theme if theme and theme != 'all' else 'all'
        output_file = f"api/random-quote-{theme_suffix}.json"
    
    quote = generate_random_quote(theme_filter=theme)
    
    # Create api directory if it doesn't exist
    output_path = Path(__file__).parent / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(quote, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Quote saved to {output_file}")
    print(f"  Theme: {quote.get('theme', 'Unknown')}")
    print(f"  Text: {quote['text'][:50]}...")
    print(f"  Author: {quote['author']}")
    return quote


def generate_all_theme_files():
    """Generate a random quote file for each theme + 'all' themes"""
    all_quotes = load_quotes()
    
    # Get unique themes from quotes
    themes = sorted(set(q.get('theme', '').lower() for q in all_quotes if q.get('theme')))
    themes = ['all'] + themes  # Add 'all' option first
    
    print("\n🎬 Generating quote files for all themes...\n")
    
    generated_files = []
    for theme in themes:
        try:
            quote = save_random_quote(theme=theme)
            generated_files.append((theme, quote))
        except Exception as e:
            print(f"❌ Error generating {theme}: {e}")
    
    print(f"\n✅ Successfully generated {len(generated_files)} files:")
    for theme, quote in generated_files:
        print(f"   - api/random-quote-{theme}.json")
    
    return generated_files


if __name__ == "__main__":
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        theme_arg = sys.argv[1]
        print(f"Generating quote for theme: {theme_arg}")
        save_random_quote(theme=theme_arg)
    else:
        # Generate all theme files by default
        generate_all_theme_files()
