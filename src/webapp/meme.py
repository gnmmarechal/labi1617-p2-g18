from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from misc_module import remove_extension as rem_ext


def meme_image(file_name, effect_name, args=None):
    try:
        im = effect_name(Image.open(file_name), args)
        im.save(rem_ext(file_name)+".png")
        return 0
    except Exception: # Returns -1 if an exception is thrown. This is done to avoid any crashes.
        return -1


def add_text(im, args):
    if len(args) != 3 and len(args) != 2:
        raise Exception("Wrong argument length")
    outline = args[0]
    text = args[1].upper()
    text_up = ""
    if len(args) == 3:
        text_up = args[2].upper()
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("impact.ttf", 40)
    w, h = draw.textsize(text, font=font)
    iw, ih = im.size

    # Bottom Text
    if outline:
        draw.text(((iw-w)/2-1, ih*0.8-1), text, (0, 0, 0), font=font)
        draw.text(((iw-w)/2+1, ih*0.8-1), text, (0, 0, 0), font=font)
        draw.text(((iw-w)/2-1, ih*0.8+1), text, (0, 0, 0), font=font)
        draw.text(((iw-w)/2+1, ih*0.8+1), text, (0, 0, 0), font=font)

    draw.text(((iw-w)/2, ih*0.8), text, (255, 255, 255), font=font)

    # Top Text
    if len(args) == 3:
        if outline:
            draw.text(((iw-w)/2-1, ih*0.05-1), text_up, (0, 0, 0), font=font)
            draw.text(((iw-w)/2+1, ih*0.05-1), text_up, (0, 0, 0), font=font)
            draw.text(((iw-w)/2-1, ih*0.05+1), text_up, (0, 0, 0), font=font)
            draw.text(((iw-w)/2+1, ih*0.05+1), text_up, (0, 0, 0), font=font)

        draw.text(((iw-w)/2, ih*0.05), text_up, (255, 255, 255), font=font)

    return im


# Black and White -> Sepia from effects.py
def black_and_white(im):
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


# Cut background
def remove_background(im):

    im = im.convert("RGBA")

    pixdata = im.load()

    width, height = im.size

    for x in range(width):
        for y in range(height):
            if pixdata[x, y] == (123,123,123,255): #123 -> Valor em que os pixeis mudam
                pixdata[x, y] = (123,123,123,0)

    return im

#Apply another background
def applybackground(im,args):



    return im

#Help pls
