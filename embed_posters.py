#!/usr/bin/env python3
"""
Embed base64-encoded poster images into shared-posters.liquid template

This script reads movie poster images from assets/posters-small, encodes them as base64,
and embeds them into the shared-posters.liquid template for use in TRMNL layouts.

Usage:
    python3 embed_posters.py

Output:
    Updates templates/shared-posters.liquid with inline base64-encoded images
"""

import os
import base64
from pathlib import Path


def embed_posters():
    """Read poster images and embed them as base64 into shared-posters.liquid"""
    
    # Paths
    project_root = Path(__file__).parent
    poster_dir = project_root / 'assets' / 'posters-small'
    shared_file = project_root / 'templates' / 'shared-posters.liquid'
    
    # Define posters to embed (in order)
    poster_files = [
        'kung-fu-panda-1-poster.jpeg',
        'kung-fu-panda-2-poster.jpeg',
        'kung-fu-panda-3-poster.jpeg',
        'kung-fu-panda-4-poster.jpg'
    ]
    
    # Read and encode poster images
    posters = {}
    for i, filename in enumerate(poster_files, 1):
        poster_path = poster_dir / filename
        
        if not poster_path.exists():
            print(f"❌ File not found: {poster_path}")
            return False
        
        with open(poster_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            posters[i] = base64_data
            file_size = len(image_data)
            print(f"✅ Encoded kung-fu-panda-{i}-poster ({file_size:,} bytes → {len(base64_data):,} bytes base64)")
    
    # Read shared-posters.liquid template
    if not shared_file.exists():
        print(f"❌ shared-posters.liquid not found at {shared_file}")
        return False
    
    with open(shared_file, 'r') as f:
        content = f.read()
    
    # Determine MIME type for each image
    mime_types = {
        1: 'image/jpeg',
        2: 'image/jpeg',
        3: 'image/jpeg',
        4: 'image/jpeg'
    }
    
    # Replace capture blocks with base64-encoded images
    import re
    
    for i in range(1, 5):
        pattern = rf'({{%- capture poster_kfp_{i} -%}})[\s\S]*?({{%- endcapture -%}})'
        replacement = rf'\1\ndata:{mime_types[i]};base64,{posters[i]}\n\2'
        content = re.sub(pattern, replacement, content)
    
    # Write updated file
    with open(shared_file, 'w') as f:
        f.write(content)
    
    total_size = os.path.getsize(shared_file)
    print(f"\n✅ Successfully embedded all 4 posters into shared-posters.liquid")
    print(f"📄 Template file size: {total_size:,} bytes")
    print(f"\n📋 Usage in your .liquid templates:")
    print(f"   {{% if movie == 'Kung Fu Panda' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_1 }}}}\" />")
    print(f"   {{% elsif movie == 'Kung Fu Panda 2' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_2 }}}}\" />")
    print(f"   {{% elsif movie == 'Kung Fu Panda 3' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_3 }}}}\" />")
    print(f"   {{% elsif movie == 'Kung Fu Panda 4' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_4 }}}}\" />")
    print(f"   {{% endif %}}")
    
    return True


if __name__ == '__main__':
    success = embed_posters()
    if not success:
        print("\n❌ Failed to embed posters. Please check the error messages above.")
        exit(1)
