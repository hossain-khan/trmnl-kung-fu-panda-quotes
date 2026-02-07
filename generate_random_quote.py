#!/usr/bin/env python3
"""
Generate random Kung Fu Panda quotes by theme
This script creates theme-specific API endpoint files for TRMNL
Features quote history tracking to prevent repeats within 30 days
"""

import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path


# Constants for quote history tracking
HISTORY_FILE = Path(__file__).parent / '.quote-history.json'
DAYS_BEFORE_REUSE = 30  # Don't reuse quotes within 30 days


def load_quote_history():
    """Load quote history from file
    
    Returns:
        Dictionary with 'quotes' list containing recently used quotes
    """
    if not HISTORY_FILE.exists():
        return {'quotes': []}
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'quotes': []}


def save_quote_history(history):
    """Save quote history to file
    
    Args:
        history: Dictionary with 'quotes' list
    """
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def cleanup_old_history(history):
    """Remove quotes older than DAYS_BEFORE_REUSE from history
    
    Args:
        history: Dictionary with 'quotes' list
    
    Returns:
        Cleaned history dictionary
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_BEFORE_REUSE)
    
    cleaned_quotes = []
    for entry in history.get('quotes', []):
        try:
            selected_date = datetime.fromisoformat(entry['selected_on'].replace('Z', '+00:00'))
            if selected_date > cutoff_date:
                cleaned_quotes.append(entry)
        except (KeyError, ValueError):
            # Skip entries with invalid or missing dates
            continue
    
    return {'quotes': cleaned_quotes}


def get_recently_used_quote_ids(history):
    """Get set of quote IDs used within DAYS_BEFORE_REUSE
    
    Args:
        history: Dictionary with 'quotes' list
    
    Returns:
        Set of quote IDs (integers)
    """
    return {entry['id'] for entry in history.get('quotes', []) if 'id' in entry}


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
    Tracks quote history to prevent repeats within 30 days
    
    Args:
        theme_filter: Theme to filter by (e.g., 'wisdom', 'humor'), or None for all quotes
    
    Returns:
        Dictionary containing quote data with timestamp
    """
    all_quotes = load_quotes()
    
    # Load and cleanup history
    history = load_quote_history()
    history = cleanup_old_history(history)
    recently_used_ids = get_recently_used_quote_ids(history)
    
    # Filter by theme if specified
    if theme_filter and theme_filter.lower() != 'all':
        filtered_quotes = [q for q in all_quotes if q.get('theme', '').lower() == theme_filter.lower()]
        if not filtered_quotes:
            print(f"⚠️  No quotes found for theme '{theme_filter}', using all quotes")
            filtered_quotes = all_quotes
        quotes = filtered_quotes
    else:
        quotes = all_quotes
    
    # Filter out recently used quotes
    available_quotes = [q for q in quotes if q.get('id') not in recently_used_ids]
    
    # Fallback: If all quotes have been used recently, reset and use all quotes
    if not available_quotes:
        print(f"ℹ️  All quotes in this theme have been used recently. Resetting history.")
        available_quotes = quotes
        # Clear history for this theme
        history = {'quotes': []}
    
    # Select random quote from available ones
    quote = random.choice(available_quotes)
    
    # Add timestamp
    quote['updated_on'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Record this quote in history
    history_entry = {
        'id': quote.get('id'),
        'text': quote.get('text'),
        'author': quote.get('author'),
        'movie': quote.get('movie'),
        'theme': quote.get('theme'),
        'selected_on': quote['updated_on']
    }
    history['quotes'].append(history_entry)
    save_quote_history(history)
    
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
