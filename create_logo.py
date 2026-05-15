from PIL import Image, ImageDraw

# Create a new image with white background
width, height = 200, 100
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Draw orange curved line (top decorative element)
draw.arc([20, 10, 180, 90], 0, 180, fill='#FF8C00', width=8)

# Draw dark blue curved lines (on the left)
draw.arc([30, 30, 80, 120], 180, 360, fill='#1A1F71', width=5)
draw.arc([50, 30, 100, 120], 180, 360, fill='#1A1F71', width=5)
draw.arc([70, 30, 120, 120], 180, 360, fill='#1A1F71', width=5)

# Draw circle (on the top right)
draw.ellipse([130, 15, 160, 45], fill='#1A1F71')

# Save the image
image.save('tasma_logo.png')
print("✓ TASMA logo created: tasma_logo.png")
