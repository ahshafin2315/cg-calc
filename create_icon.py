from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=(256, 256)):
    # Create base image with transparency
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use Impact font with very large size
        font = ImageFont.truetype('impact.ttf', size=200)
    except:
        try:
            # Fallback to Arial
            font = ImageFont.truetype('arial.ttf', size=200)
        except:
            # Last resort: default font
            font = ImageFont.load_default()
    
    text = "CG"
    
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center position
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - 40  # Shift up by 20 pixels for better optical centering
    
    # Draw shadow (reduced offset for cleaner look)
    draw.text((x+4, y+4), text, fill=(0, 0, 0, 160), font=font)
    
    # Draw main text in bright blue
    draw.text((x, y), text, fill=(30, 144, 255, 255), font=font)
    
    # Save icon
    icon_path = 'app_icon.ico'
    img.save(icon_path, format='ICO', sizes=[(256, 256)])
    print(f"Icon created: {os.path.abspath(icon_path)}")

if __name__ == "__main__":
    create_icon()
