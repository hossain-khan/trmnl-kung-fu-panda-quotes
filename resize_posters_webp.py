#!/usr/bin/env python3
"""
Resize poster images to WebP format to be under 15KB while maintaining aspect ratio.
This script uses cwebp for WebP conversion to achieve better compression than PNG.
"""

import os
import subprocess
from PIL import Image
import sys

# Configuration
SOURCE_DIR = "assets/posters-small-bw-outline"
TARGET_MAX_SIZE = 15 * 1024  # 15KB in bytes
OUTPUT_SUFFIX = "-webp"

# Test widths to try (in descending order) - starting higher since WebP compresses better
TEST_WIDTHS = [300, 280, 260, 240, 220, 200, 180, 160, 140, 120, 100, 90, 80, 70, 60, 50]


def get_file_size(filepath):
    """Get file size in bytes."""
    return os.path.getsize(filepath)


def resize_and_convert_to_webp(input_path, output_path, target_width, quality=80):
    """
    Resize image to target width and convert to WebP format.
    Returns the output file size in bytes.
    """
    temp_png = output_path + ".temp.png"
    
    try:
        # First resize with PIL
        with Image.open(input_path) as img:
            # Calculate new height maintaining aspect ratio
            aspect_ratio = img.height / img.width
            target_height = int(target_width * aspect_ratio)
            
            # Resize with high-quality resampling
            resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Save as temp PNG
            resized.save(temp_png, 'PNG')
        
        # Convert to WebP using cwebp
        cmd = [
            'cwebp',
            '-q', str(quality),  # Quality setting
            '-m', '6',  # Compression method (0-6, 6 is slowest but best)
            temp_png,
            '-o', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"\n    ⚠️  cwebp error: {result.stderr}")
            return float('inf')
        
        # Clean up temp file
        if os.path.exists(temp_png):
            os.remove(temp_png)
        
        return get_file_size(output_path)
        
    except Exception as e:
        print(f"\n    ⚠️  Error: {e}")
        if os.path.exists(temp_png):
            os.remove(temp_png)
        return float('inf')


def find_optimal_width(input_path, temp_output_path, target_size):
    """
    Find the largest width that results in file size under target_size.
    Returns optimal width and resulting file size.
    """
    best_width = None
    best_size = float('inf')
    
    print(f"\n  Testing widths for {os.path.basename(input_path)}:")
    
    for width in TEST_WIDTHS:
        file_size = resize_and_convert_to_webp(input_path, temp_output_path, width)
        size_kb = file_size / 1024
        
        print(f"    Width {width:3d}px -> {size_kb:6.2f} KB", end="")
        
        if file_size <= target_size:
            print(" ✓ (under 15KB)")
            if best_width is None or width > best_width:
                best_width = width
                best_size = file_size
                # Found the optimal (we test in descending order, so first match is best)
                break
        else:
            print(" ✗ (too large)")
    
    return best_width, best_size


def process_images():
    """Process all PNG files in the source directory."""
    # Find all PNG files (only originals, not optimized versions)
    png_files = [f for f in os.listdir(SOURCE_DIR) 
                 if f.endswith('.png') and '-optimized' not in f and '-webp' not in f]
    
    if not png_files:
        print(f"No PNG files found in {SOURCE_DIR}")
        return
    
    print(f"Found {len(png_files)} images to process")
    print(f"Target: under {TARGET_MAX_SIZE / 1024:.0f} KB (WebP format)")
    print("=" * 60)
    
    results = []
    
    for filename in sorted(png_files):
        input_path = os.path.join(SOURCE_DIR, filename)
        base_name = filename.replace('.png', '')
        output_filename = f"{base_name}{OUTPUT_SUFFIX}.webp"
        output_path = os.path.join(SOURCE_DIR, output_filename)
        temp_output = output_path + ".tmp"
        
        # Get original size
        original_size = get_file_size(input_path)
        original_size_kb = original_size / 1024
        
        with Image.open(input_path) as img:
            original_dims = f"{img.width}x{img.height}"
        
        print(f"\n📸 {filename}")
        print(f"   Original: {original_size_kb:.2f} KB ({original_dims})")
        
        # Find optimal width
        optimal_width, final_size = find_optimal_width(input_path, temp_output, TARGET_MAX_SIZE)
        
        if optimal_width:
            # Now create the final image at optimal width
            print(f"\n   Creating final WebP at {optimal_width}px...")
            resize_and_convert_to_webp(input_path, output_path, optimal_width)
            final_size = get_file_size(output_path)
            
            # Clean up temp file
            if os.path.exists(temp_output):
                os.remove(temp_output)
            
            # Get final dimensions
            with Image.open(input_path) as img:
                aspect_ratio = img.height / img.width
                final_height = int(optimal_width * aspect_ratio)
            
            final_size_kb = final_size / 1024
            reduction_pct = ((original_size - final_size) / original_size) * 100
            
            print(f"\n   ✅ Optimized: {optimal_width}x{final_height}px -> {final_size_kb:.2f} KB ({reduction_pct:.1f}% reduction)")
            
            results.append({
                'filename': filename,
                'optimal_width': optimal_width,
                'optimal_height': final_height,
                'original_kb': original_size_kb,
                'final_kb': final_size_kb,
                'reduction_pct': reduction_pct
            })
        else:
            print(f"\n   ❌ Could not find size under {TARGET_MAX_SIZE / 1024:.0f} KB")
            if os.path.exists(temp_output):
                os.remove(temp_output)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY - WebP Format")
    print("=" * 60)
    
    if results:
        for result in results:
            print(f"\n{result['filename']}")
            print(f"  Dimensions: {result['optimal_width']}x{result['optimal_height']}px")
            print(f"  Original:   {result['original_kb']:.2f} KB")
            print(f"  Optimized:  {result['final_kb']:.2f} KB")
            print(f"  Saved:      {result['reduction_pct']:.1f}%")
        
        avg_width = sum(r['optimal_width'] for r in results) / len(results)
        avg_reduction = sum(r['reduction_pct'] for r in results) / len(results)
        
        print("\n" + "-" * 60)
        print(f"Average optimal width: {avg_width:.0f}px")
        print(f"Average size reduction: {avg_reduction:.1f}%")
        print(f"\nWebP files saved with '{OUTPUT_SUFFIX}' suffix")
        
        # Compare with PNG version
        print("\n💡 Comparison with PNG optimization:")
        print(f"   PNG optimal width: 100px")
        print(f"   WebP optimal width: {avg_width:.0f}px")
        print(f"   WebP improvement: {(avg_width / 100 - 1) * 100:.0f}% larger images!")
    else:
        print("No images were successfully optimized.")


if __name__ == "__main__":
    # Check if cwebp is available
    try:
        result = subprocess.run(['which', 'cwebp'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Error: cwebp not found. Please install via: brew install webp")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking for cwebp: {e}")
        sys.exit(1)
    
    try:
        process_images()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
