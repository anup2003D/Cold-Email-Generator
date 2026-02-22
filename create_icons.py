"""
Simple script to create placeholder extension icons
Run this if you don't have icons yet
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    
    def create_icon(size, filename):
        # Create image with gradient-like purple background
        img = Image.new('RGB', (size, size), color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Add a simple envelope shape
        if size >= 48:
            # Draw simple envelope
            margin = size // 4
            draw.rectangle(
                [margin, margin, size - margin, size - margin],
                fill='white',
                outline='#764ba2',
                width=2
            )
            # Envelope flap
            center = size // 2
            draw.line(
                [margin, margin, center, center],
                fill='#764ba2',
                width=2
            )
            draw.line(
                [size - margin, margin, center, center],
                fill='#764ba2',
                width=2
            )
        
        img.save(filename)
        print(f"Created {filename}")
    
    # Create icons
    import os
    os.makedirs('extension/icons', exist_ok=True)
    
    create_icon(16, 'extension/icons/icon16.png')
    create_icon(48, 'extension/icons/icon48.png')
    create_icon(128, 'extension/icons/icon128.png')
    
    print("\n✅ All icons created successfully!")
    print("You can now load the extension in Chrome.")
    
except ImportError:
    print("PIL/Pillow not installed.")
    print("\nCreating simple colored square icons instead...\n")
    
    # Fallback: Create simple colored squares using base64
    import base64
    import os
    
    os.makedirs('extension/icons', exist_ok=True)
    
    # Simple 1x1 purple pixel PNG (base64 encoded)
    purple_pixel = base64.b64decode(
        b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    )
    
    for size in [16, 48, 128]:
        filename = f'extension/icons/icon{size}.png'
        with open(filename, 'wb') as f:
            f.write(purple_pixel)
        print(f"Created {filename} (placeholder)")
    
    print("\n✅ Placeholder icons created!")
    print("⚠️  These are minimal placeholders. For better icons:")
    print("   - Install Pillow: pip install Pillow")
    print("   - Run this script again")
    print("   - Or create custom icons at https://favicon.io/")
