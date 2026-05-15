from PIL import Image, ImageDraw, ImageFont

# Create a new image with white background
width, height = 300, 150
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Colors
orange = '#FF8C00'
dark_blue = '#1A1F71'

# Draw orange curved line (top decorative element - like a swoosh)
draw.arc([80, 0, 220, 100], 0, 180, fill=orange, width=12)

# Draw dark blue circle (top right)
draw.ellipse([140, 15, 175, 50], fill=dark_blue)

# Draw dark blue curved lines (on the left - like speed marks)
# Line 1 (leftmost, most curved)
draw.line([(70, 40), (120, 80)], fill=dark_blue, width=8)
draw.line([(85, 30), (130, 85)], fill=dark_blue, width=8)

# Line 2 (middle)
draw.line([(90, 35), (135, 85)], fill=dark_blue, width=8)
draw.line([(105, 25), (150, 85)], fill=dark_blue, width=8)

# Line 3 (rightmost)
draw.line([(110, 45), (155, 95)], fill=dark_blue, width=8)
draw.line([(125, 35), (170, 95)], fill=dark_blue, width=8)

# Try to add text - TASMA in orange and GROUP in dark blue
try:
    # Use a built-in font (fallback)
    font_large = ImageFont.load_default()
    
    # Draw "TASMA" in orange
    draw.text((100, 110), "TASMA", fill=orange, font=font_large)
    
    # Draw "GROUP" in dark blue
    draw.text((185, 120), "GROUP", fill=dark_blue, font=font_large)
except:
    pass

# Save the image
image.save('tasma_logo.png')
print("✓ TASMA GROUP logo created: tasma_logo.png")
