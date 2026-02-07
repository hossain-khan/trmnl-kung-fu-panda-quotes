#!/usr/bin/env python3
"""
Embed base64-encoded BW outline poster images (WebP format) into shared-posters.liquid template

This script reads movie poster BW outline images from assets/posters-small-bw-outline, 
encodes them as base64, and embeds them into the shared-posters.liquid template 
for use in TRMNL layouts.

Usage:
    python3 embed_posters_bw_outline.py

Output:
    Updates templates/shared-posters.liquid with inline base64-encoded WebP images
    as poster_kfp_1_bw, poster_kfp_2_bw, poster_kfp_3_bw, poster_kfp_4_bw
"""

import os
import base64
from pathlib import Path


def embed_bw_outline_posters():
    """Read BW outline poster images and embed them as base64 into shared-posters.liquid"""
    
    # Paths
    project_root = Path(__file__).parent
    poster_dir = project_root / 'assets' / 'posters-small-bw-outline'
    shared_file = project_root / 'templates' / 'shared-posters.liquid'
    
    # Define posters to embed (in order)
    poster_files = [
        'kung-fu-panda-1-poster-bw-outline-webp.webp',
        'kung-fu-panda-2-poster-bw-outline-webp.webp',
        'kung-fu-panda-3-poster-bw-outline-webp.webp',
        'kung-fu-panda-4-poster-bw-outline-webp.webp'
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
            base64_size = len(base64_data)
            print(f"✅ Encoded kung-fu-panda-{i}-poster-bw-outline ({file_size:,} bytes → {base64_size:,} bytes base64)")
    
    # Read shared-posters.liquid template
    if not shared_file.exists():
        print(f"❌ shared-posters.liquid not found at {shared_file}")
        return False
    
    with open(shared_file, 'r') as f:
        content = f.read()
    
    # Check if BW outline blocks already exist
    import re
    
    has_bw_blocks = bool(re.search(r'{%- capture poster_kfp_1_bw -%}', content))
    
    if has_bw_blocks:
        # Update existing blocks
        print("\n🔄 Updating existing BW outline poster blocks...")
        for i in range(1, 5):
            pattern = rf'({{%- capture poster_kfp_{i}_bw -%}})[\s\S]*?({{%- endcapture -%}})'
            replacement = rf'\1\ndata:image/webp;base64,{posters[i]}\n\2'
            content = re.sub(pattern, replacement, content)
    else:
        # Add new blocks at the end
        print("\n➕ Adding new BW outline poster blocks...")
        
        # Add comment and blocks before the final closing
        bw_blocks = "\n\n{%- comment -%}\nBlack & White Outline Posters (WebP format, optimized for e-ink)\n{%- endcomment -%}\n\n"
        
        for i in range(1, 5):
            bw_blocks += f"{{%- capture poster_kfp_{i}_bw -%}}\n"
            bw_blocks += f"data:image/webp;base64,{posters[i]}\n"
            bw_blocks += f"{{%- endcapture -%}}\n\n"
        
        # Append to end of file
        content += bw_blocks.rstrip() + "\n"
    
    # Write updated file
    with open(shared_file, 'w') as f:
        f.write(content)
    
    total_size = os.path.getsize(shared_file)
    print(f"\n✅ Successfully embedded all 4 BW outline posters into shared-posters.liquid")
    print(f"📄 Template file size: {total_size:,} bytes ({total_size / 1024:.2f} KB)")
    print(f"\n📋 Usage in your .liquid templates:")
    print(f"   {{% if movie == 'Kung Fu Panda' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_1_bw }}}}\" class=\"image image-dither\" />")
    print(f"   {{% elsif movie == 'Kung Fu Panda 2' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_2_bw }}}}\" class=\"image image-dither\" />")
    print(f"   {{% elsif movie == 'Kung Fu Panda 3' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_3_bw }}}}\" class=\"image image-dither\" />")
    print(f"   {{% elsif movie == 'Kung Fu Panda 4' %}}")
    print(f"     <img src=\"{{{{ poster_kfp_4_bw }}}}\" class=\"image image-dither\" />")
    print(f"   {{% endif %}}")
    print(f"\n💡 Benefits:")
    print(f"   • WebP format: 70% larger images vs PNG (160-200px vs 100px)")
    print(f"   • All under 15KB per image")
    print(f"   • Optimized for e-ink displays")
    print(f"   • Black & white outline style for better contrast")
    
    return True


if __name__ == '__main__':
    success = embed_bw_outline_posters()
    if not success:
        print("\n❌ Failed to embed BW outline posters. Please check the error messages above.")
        exit(1)
