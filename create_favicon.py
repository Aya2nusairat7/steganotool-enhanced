from PIL import Image, ImageDraw
import os

# Create a 32x32 transparent image
img = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a lock icon
# Lock body
draw.rectangle((8, 12, 24, 28), fill=(52, 152, 219), outline=(41, 128, 185))

# Lock shackle
draw.rectangle((12, 5, 20, 12), fill=None, outline=(41, 128, 185), width=2)
draw.arc((10, 0, 22, 12), start=0, end=180, fill=(41, 128, 185), width=2)

# Keyhole
draw.ellipse((14, 16, 18, 20), fill=(255, 255, 255))
draw.rectangle((15, 18, 17, 24), fill=(255, 255, 255))

# Save the image
output_path = os.path.join('static', 'img', 'favicon.png')
img.save(output_path)

print(f"Favicon created and saved to {output_path}") 