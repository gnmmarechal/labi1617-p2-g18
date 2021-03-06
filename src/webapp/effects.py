from PIL import Image
from PIL import ImageFilter
from misc_module import remove_extension as rem_ext


# Modify an image with the selected effect
def effect_image(file_name, effect_name):
    try:
        im = effect_name(Image.open(file_name))
        im.save(rem_ext(file_name)+".png")
        return 0
    except Exception as e:
        print("ERROR: " + str(e))
        return -1


# Blur effect
def blur(im):
    return im.filter(ImageFilter.BLUR)


# Lomography Effect
def lomography(im):
    nim = Image.new(im.mode, im.size)
    width, height = im.size
    for x in range(width):
        for y in range(height):
            p = im.getpixel((x, y))
            r = p[0]
            g = p[1]
            b = p[2]
            nb = int(round(r * 0.189 + g * 0.769 + b * 0.393))
            ng = int(round(r * 0.168 + g * 0.686 + b * 0.349))
            nr = int(round(r * 0.131 + g * 0.534 + b * 0.272))
            nim.putpixel((x, y), (nr, ng, nb))
    return nim


# Sepia Effect
def sepia(im):
    nim = Image.new(im.mode, im.size)
    width, height = im.size

    for x in range(width):
        for y in range(height):
            p = im.getpixel((x,y))
            r = p[0]
            g = p[1]
            b = p[2]
            nr = int(round(r * 0.189 + g * 0.769 + b * 0.393))
            ng = int(round(r * 0.168 + g * 0.686 + b * 0.349))
            nb = int(round(r * 0.131 + g * 0.534 + b * 0.272))
            nim.putpixel((x, y), (nr, ng, nb))
    return nim


# Grayscale Effect
def grayscale(im):
    return im.convert("L")


# Color Inversion
def colorinv(im, arg=None):
    nim = Image.new(im.mode, im.size)
    width, height = im.size

    for x in range(width):
        for y in range(height):
            p = im.getpixel((x,y))
            r = 255-p[0]
            g = 255-p[1]
            b = 255-p[2]
            nim.putpixel((x,y), (r,g,b))
    return nim

