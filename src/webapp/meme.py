from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from misc_module import remove_extension as rem_ext

def meme_image(file_name, effect_name, args=None):
    try:
        im = effect_name(Image.open(file_name), args)
        im.save(rem_ext(file_name)+".png")
        return 0
    except Exception:
        return -1

def addtext(im, args):
	outline = args[1]
	text = args[0].upper()
	draw = ImageDraw.Draw(im)
	font = ImageFont.truetype("impact.ttf",30)
	w, h = draw.textsize(text, font=font)
	iw, ih = im.size
	
	if outline:
		draw.text(((iw-w)/2-1,ih*0.75-1), text, (0,0,0), font=font)
		draw.text(((iw-w)/2+1,ih*0.75-1), text, (0,0,0), font=font)
		draw.text(((iw-w)/2-1,ih*0.75+1), text, (0,0,0), font=font)
		draw.text(((iw-w)/2+1,ih*0.75+1), text, (0,0,0), font=font)
	
	draw.text(((iw-w)/2,ih*0.75), text, (255,255,255), font=font)

	return im
