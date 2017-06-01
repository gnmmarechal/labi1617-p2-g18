from PIL import Image
from misc_module import remove_extension as rem_ext


# Modify an image with the selected effect
def effect_image(file_name, effect_name):
    try:
        im = effect_name(Image.open(file_name))
        im.save(rem_ext(file_name)+".png")
        return 0
    except Exception:
        return -1


# Grayscale Effect
def grayscale(im):
    return im.convert("L")

print(effect_image("1.jpg", grayscale))