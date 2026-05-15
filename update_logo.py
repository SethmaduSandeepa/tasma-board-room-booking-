from PIL import Image, ImageDraw

# Create a new image with light background
width, height = 350, 150
image = Image.new('RGB', (width, height), color='#f5f5f5')
draw = ImageDraw.Draw(image)

# Colors
orange = '#FF8C00'
dark_blue = '#1A1F71'
gray = '#555555'

# Draw orange swoosh curve (bottom)
# Quarter circle for the swoosh
for i in range(0, 120, 2):
    y_offset = int((i ** 2) / 400)
    draw.ellipse([80 + i - 8, 80 + y_offset - 8, 80 + i + 8, 80 + y_offset + 8], fill=orange)

# Smoother orange curve using arc
draw.arc([50, 40, 250, 140], 0, 90, fill=orange, width=10)

# Draw dark blue circle (top right)
circle_x, circle_y = 130, 30
circle_radius = 18
draw.ellipse([circle_x - circle_radius, circle_y - circle_radius, 
              circle_x + circle_radius, circle_y + circle_radius], 
             fill=dark_blue)

# Draw dark blue diagonal speed lines (left side)
# Line 1 (leftmost)
draw.line([(50, 35), (95, 85)], fill=dark_blue, width=7)

# Line 2 (middle-left)
draw.line([(65, 25), (110, 80)], fill=dark_blue, width=7)

# Line 3 (middle)
draw.line([(80, 20), (125, 75)], fill=dark_blue, width=7)

# Line 4 (middle-right)
draw.line([(95, 25), (140, 80)], fill=dark_blue, width=7)

# Line 5 (rightmost)
draw.line([(110, 35), (155, 90)], fill=dark_blue, width=7)

# Add text
try:
    # Try to draw "TASMA" and "GROUP"
    from PIL import ImageFont
    
    # Draw TASMA in orange - positioned below the lines
    draw.text((70, 110), "TASMA", fill=orange, font=ImageFont.load_default())
    
    # Draw GROUP in gray/dark - positioned to the right
    draw.text((180, 110), "GROUP", fill=gray, font=ImageFont.load_default())
except:
    pass

# Save the image
image.save('tasma_logo.png')
print("✓ TASMA GROUP logo updated: tasma_logo.png")
