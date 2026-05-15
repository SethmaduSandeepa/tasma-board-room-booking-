from PIL import Image, ImageDraw, ImageFont

# Create a new image with white background matching the provided logo
width, height = 450, 250
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image, 'RGBA')

# Colors from the TASMA GROUP logo
orange = '#FF8C00'
dark_blue = '#1A1F71'

# Draw orange swoosh (large curved line at top)
# Using bezier-like curve for the swoosh
draw.arc([20, -100, 420, 200], 0, 90, fill=orange, width=35)

# Draw dark blue circle (top right)
circle_x, circle_y = 145, 30
circle_radius = 28
draw.ellipse([circle_x - circle_radius, circle_y - circle_radius, 
              circle_x + circle_radius, circle_y + circle_radius], 
             fill=dark_blue)

# Draw dark blue curved speed lines (left side) - more pronounced curves
# Using thick lines with curves
line_coords = [
    # Line 1 (leftmost, most curved)
    [(30, 50), (110, 140)],
    # Line 2 
    [(55, 35), (130, 145)],
    # Line 3 (middle)
    [(80, 30), (155, 150)],
    # Line 4
    [(95, 50), (170, 160)],
    # Line 5 (rightmost)
    [(115, 80), (185, 165)],
]

for coords in line_coords:
    draw.line(coords, fill=dark_blue, width=12)

# Add text - TASMA in orange and GROUP in dark blue
try:
    # Try to use a larger font if available
    tasma_font = ImageFont.load_default()
    group_font = ImageFont.load_default()
    
    # Draw "TASMA" in large orange letters
    draw.text((155, 180), "TASMA", fill=orange, font=tasma_font)
    
    # Draw "GROUP" in dark blue, smaller
    draw.text((300, 200), "GROUP", fill=dark_blue, font=group_font)
    
except:
    pass

# Save the image
image.save('tasma_logo.png')
print("✓ TASMA GROUP logo created to match the provided design")
