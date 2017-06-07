from PIL import Image
from PIL import ImageDraw
from misc_module import remove_extension as rem_ext

def effect_image(file_name, args=None):
    try:
        im = Image.open(file_name)
        im.save(rem_ext(file_name)+".png")
        return 0
    except Exception:
        return -1

def addtext(im, text):
	
	draw = ImageDraw.Draw(im)
	font = ImageFont.truetype("pathtofont".ttf",40)
	
	draw.text( (600,340), text, (255,255,255), font=font)
