#Coded on Python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from misc_module import remove_extension as rem_ext
import numpy as np
import cv2
#OpenCV2 was used for face recognition

def meme_image(file_name, effect_name, args=None):
    try:
        im = effect_name(Image.open(file_name), args)
        im.save(rem_ext(file_name)+".png")
        return 0
    except Exception as e:
        print("ERROR: " + str(e))
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
    fontdw = ImageFont.truetype("impact.ttf", 30)
    fontup = ImageFont.truetype("impact.ttf", 40)
    w, h = draw.textsize(text, font=fontdw)
    wu, hu = draw.textsize(text_up, font=fontup)
    iw, ih = im.size

    # Bottom Text
    if outline:
        draw.multiline_text(((iw-w)/2-1, ih*0.8-1), text, (0, 0, 0), font=fontdw, align = "center")
        draw.multiline_text(((iw-w)/2+1, ih*0.8-1), text, (0, 0, 0), font=fontdw, align = "center")
        draw.multiline_text(((iw-w)/2-1, ih*0.8+1), text, (0, 0, 0), font=fontdw, align = "center")
        draw.multiline_text(((iw-w)/2+1, ih*0.8+1), text, (0, 0, 0), font=fontdw, align = "center")

    draw.multiline_text(((iw-w)/2, ih*0.8), text, (255, 255, 255), font=fontdw, align = "center")

    # Top Text
    if len(args) == 3:
        if outline:
            draw.multiline_text(((iw-wu)/2-1, -1), text_up, (0, 0, 0), font=fontup, align = "center")
            draw.multiline_text(((iw-wu)/2+1, -1), text_up, (0, 0, 0), font=fontup, align = "center")
            draw.multiline_text(((iw-wu)/2-1, +1), text_up, (0, 0, 0), font=fontup, align = "center")
            draw.multiline_text(((iw-wu)/2+1, +1), text_up, (0, 0, 0), font=fontup, align = "center")

        draw.multiline_text(((iw-wu)/2, 0), text_up, (255, 255, 255), font=fontup, align = "center")

    return im


# Black and White -> Sepia from effects.py
def black_and_white(im,args=None):
	 return im.convert("L")

#Cut face from image
#Apply another background
#file_name is the background
#The app should call face.py 1st, and then apply bkgrd

def ptest(im, args=None):
	im_w, im_h = im.size
	ptr = Image.open("ptestright.png", "r")
	ptl = Image.open("ptestleft.png", "r" )

	
	offsright = (im_w-272,im_h-225)
	
	offsleft = (0,im_h-159)
	
	im.paste(ptr, offsright,ptr)
	
	im.paste(ptl, offsleft,ptl)
	
	return im

#Triangle Background
def dobgtriangle(im, args=None):

	img = np.array(im)
	img = img[:, :, ::-1].copy() 
	
	face_im = facecut(img)	
	im_w, im_h = face_im.size	
	
	bg = Image.new("RGB", (640, 480), (255, 255, 255))
	
	draw = ImageDraw.Draw(bg)
	
	draw.polygon([(0,0), (320,0), (320,240)], fill = (255,0,0))
	draw.polygon([(0,0), (0,330), (320,240)], fill = (255,125,0))
	draw.polygon([(0,330), (0,480), (320,240)], fill = (255,255,0))
	draw.polygon([(0,480), (320,480), (320,240)], fill = (0,255,0))
	draw.polygon([(320,0), (640,0), (320,240)], fill = (0,255,255))
	draw.polygon([(640,0), (640,150), (320,240)], fill = (0,0,255))
	draw.polygon([(640,150), (640,480), (320,240)], fill = (125,0,255))
	draw.polygon([(320,480), (640,480), (320,240)], fill = (255,0,255))
	
	offset = ((640 - im_w)//2, (480 - im_h)//2)
	bg.paste(face_im, offset)
	return bg

#Circle Background
def dobgcircle(im, args=None):
	
	img = np.array(im)
	img = img[:, :, ::-1].copy() 
	
	face_im = facecut(img)	
	im_w, im_h = face_im.size	
	
	
	bg = Image.new("RGB", (640, 480), (255, 255, 255))
	
	draw = ImageDraw.Draw(bg)

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
		
	offset = ((640 - im_w)//2, (480 - im_h)//2)
	bg.paste(face_im, offset)
	return bg


#IMPORTANT NOTE
#This function was adapted from different
#http://gregblogs.com/computer-vision-cropping-faces-from-images-using-opencv2/
#http://docs.opencv.org/trunk/d7/d8b/tutorial_py_face_detection.html
#https://realpython.com/blog/python/face-recognition-with-python/

def facecut(img,args=None):

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	
	
	height = img.shape[0]
	width = img.shape[1]
	size = height * width

	if size > (500^2):
		r = 500.0 / img.shape[1]
		dim = (500, int(img.shape[0] * r))
		img2 = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
		img = img2
	#Convert from Color to Gray
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	eyesn = 0

	for (x,y,w,h) in faces:
		imgCrop = img[y:y+h,x:x+w]
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]

		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			eyesn = eyesn +1
		if eyesn >= 2:
			imgCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2RGB)
			im_pil = Image.fromarray(imgCrop)
			#im_pil.save("face"+file_name+".png")
			return im_pil
