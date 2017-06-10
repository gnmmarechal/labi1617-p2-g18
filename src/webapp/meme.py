#Coded on Python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from misc_module import remove_extension as rem_ext
#from face import *

#outline está sempre true

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
    wu, hu = draw.textsize(text_up, font=font)
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
            draw.text(((iw-wu)/2-1, hu-1), text_up, (0, 0, 0), font=font)
            draw.text(((iw-wu)/2+1, hu-1), text_up, (0, 0, 0), font=font)
            draw.text(((iw-wu)/2-1, hu+1), text_up, (0, 0, 0), font=font)
            draw.text(((iw-wu)/2+1, hu+1), text_up, (0, 0, 0), font=font)

        draw.text(((iw-wu)/2, hu), text_up, (255, 255, 255), font=font)

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

#Cut face from image
#Apply another background
#file_name is the background
#The app should call face.py 1st, and then apply bkgrd
def addbackground(im):
	im_w, im_h = im.size
	
	background = Image.new("RGBA", (640, 480), (255, 255, 255, 255))
	
	offset = ((640 - img_w)/2, (480 - img_h)/2)
	background.paste(im, offset)
	background.save("out.png")
	return background

#Testing bg
def dobg():
	
	im = Image.new("RGB", (640, 480), (255, 255, 255))
	
	draw = ImageDraw.Draw(im)
	
	draw.polygon([(0,0), (320,0), (320,240)], fill = (255,0,0))
	draw.polygon([(0,0), (0,330), (320,240)], fill = (255,125,0))
	draw.polygon([(0,330), (0,480), (320,240)], fill = (255,255,0))
	draw.polygon([(0,480), (320,480), (320,240)], fill = (0,255,0))
	draw.polygon([(320,0), (640,0), (320,240)], fill = (0,255,255))
	draw.polygon([(640,0), (640,150), (320,240)], fill = (0,0,255))
	draw.polygon([(640,150), (640,480), (320,240)], fill = (125,0,255))
	draw.polygon([(320,480), (640,480), (320,240)], fill = (255,0,255))
	
	
	im.save("color.png")
	
def dobg2():
	
	im = Image.new("RGB", (640, 480), (255, 255, 255))
	
	draw = ImageDraw.Draw(im)
	#320,240
	draw.polygon([(0,0),(0,480),(640,480),(640,0)], fill = (255,0,150))
	draw.ellipse((-40,-120, 680, 600), fill = (255,0,255), outline ='black')
	draw.ellipse((-20,-100, 660, 580), fill = (150,0,255), outline ='black')
	draw.ellipse((0,-80, 640, 560), fill = (0,0,255), outline ='black')
	draw.ellipse((20,-60, 620, 540), fill = (0,150,255), outline ='black')
	draw.ellipse((40,-40, 600, 520), fill = (0,255,255), outline ='black')
	draw.ellipse((60,-20, 580, 500), fill = (0,255,150), outline ='black')
	draw.ellipse((80,0, 560, 480), fill = (0,255,0), outline ='black')
	draw.ellipse((100,20, 540, 460), fill = (150,255,0), outline ='black')
	draw.ellipse((120,40, 520, 440), fill = (255,255,0), outline ='black')
	draw.ellipse((140,60, 500, 420), fill = (255,150,0), outline ='black')
	draw.ellipse((160,80, 480, 400), fill = (255,0,0), outline ='black')
	draw.ellipse((180,100, 460, 380), fill = (150,0,0), outline ='black')
	draw.ellipse((200,120, 440, 360), fill = 'white', outline ='black')
	draw.ellipse((240,160, 400, 320), fill = 'gray', outline ='black')
	draw.ellipse((280,200, 360, 280), fill = 'black', outline ='white')
	
	im.save("circle.png")
