#!/usr/bin/env python3
"""
Generate a random Kung Fu Panda quote
This script is used to create the API endpoint data for TRMNL
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path


def generate_random_quote():
    """Load quotes and return a random one"""
    quotes_file = Path(__file__).parent / "quotes.json"
    
    if not quotes_file.exists():
        return {
            "error": "quotes.json not found",
            "text": "There are no accidents...",
            "author": "Master Oogway",
            "movie": "Kung Fu Panda",
            "theme": "Wisdom",
            "updated_on": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
    
    with open(quotes_file, 'r', encoding='utf-8') as f:
        quotes = json.load(f)
    
    quote = random.choice(quotes)
    
    # Add timestamp
    quote['updated_on'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    return quote


def save_random_quote(output_file="api/random-quote.json"):
    """Generate quote and save to API endpoint"""
    quote = generate_random_quote()
    
    # Create api directory if it doesn't exist
    output_path = Path(__file__).parent / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(quote, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Quote saved to {output_file}")
    print(f"  Text: {quote['text'][:50]}...")
    print(f"  Author: {quote['author']}")
    return quote


if __name__ == "__main__":
    quote = save_random_quote()
    print(f"  Movie: {quote.get('movie', 'Unknown')}")
