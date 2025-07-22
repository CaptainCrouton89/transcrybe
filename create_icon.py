#!/usr/bin/env python3
"""
Simple script to create an app icon using text
"""

def create_text_icon():
    """Create a simple text-based icon"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create icon sizes
        sizes = [16, 32, 128, 256, 512]
        
        for size in sizes:
            # Create image
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Background circle
            margin = size // 10
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(70, 130, 180, 255),  # Steel blue
                        outline=(30, 90, 140, 255), width=2)
            
            # Microphone emoji or symbol
            font_size = size // 3
            try:
                # Try to use system font
                font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", font_size)
                text = "🎙️"
            except:
                # Fallback to default font with text
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                    text = "T"  # For Transcrybe
                except:
                    font = ImageFont.load_default()
                    text = "T"
            
            # Center text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2 - size // 20  # Slight adjustment
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
            
            # Save icon
            icon_name = f"icon_{size}x{size}.png"
            img.save(icon_name)
            print(f"Created {icon_name}")
        
        print("Icon files created successfully!")
        return True
        
    except ImportError:
        print("PIL (Pillow) not available. Skipping icon creation.")
        print("To create custom icons, install with: pip3 install Pillow")
        return False

if __name__ == "__main__":
    create_text_icon()