#!/usr/bin/env python3
"""
Create a simple app icon using basic shapes
"""

try:
    from PIL import Image, ImageDraw
    
    def create_icon():
        # Create 512x512 icon (macOS will resize as needed)
        size = 512
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background circle
        margin = 40
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=(70, 130, 180, 255),  # Steel blue
                    outline=(30, 90, 140, 255), width=8)
        
        # Microphone body
        mic_width = size // 6
        mic_height = size // 3
        mic_x = (size - mic_width) // 2
        mic_y = size // 3
        
        # Microphone capsule (top)
        draw.rounded_rectangle([mic_x, mic_y, mic_x + mic_width, mic_y + mic_height],
                             radius=mic_width//2, fill=(255, 255, 255, 255))
        
        # Microphone stand (bottom)
        stand_width = mic_width // 4
        stand_height = size // 6
        stand_x = (size - stand_width) // 2
        stand_y = mic_y + mic_height + 10
        
        draw.rectangle([stand_x, stand_y, stand_x + stand_width, stand_y + stand_height],
                      fill=(255, 255, 255, 255))
        
        # Base
        base_width = mic_width
        base_height = 20
        base_x = (size - base_width) // 2
        base_y = stand_y + stand_height
        
        draw.rectangle([base_x, base_y, base_x + base_width, base_y + base_height],
                      fill=(255, 255, 255, 255))
        
        # Sound waves
        for i in range(3):
            wave_radius = mic_width + (i + 1) * 30
            wave_x = size // 2 - wave_radius // 2
            wave_y = mic_y + mic_height // 2 - wave_radius // 2
            
            draw.arc([wave_x, wave_y, wave_x + wave_radius, wave_y + wave_radius],
                    start=-45, end=45, fill=(255, 255, 255, 200), width=6)
        
        # Save icon
        img.save("app_icon.png")
        print("Created app_icon.png")
        
        return True
    
    create_icon()
    
except ImportError:
    print("PIL not available, creating basic icon placeholder")
    # Create a simple text file as placeholder
    with open("app_icon.txt", "w") as f:
        f.write("🎙️ Transcrybe Icon Placeholder\n")
        f.write("Install PIL (pip3 install Pillow) to create actual icon\n")
    print("Created app_icon.txt placeholder")