from PIL import Image, ImageDraw

def create_circular_mask(size):
    """Create a circular mask for the image"""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask
