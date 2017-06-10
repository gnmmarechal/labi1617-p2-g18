import cv2
from misc_module import remove_extension as rem_ext

def meme_face(file_name, args=None):
    try:
        facecut(file_name)
        return 0
    except Exception: # Returns -1 if an exception is thrown. This is done to avoid any crashes.
        return -1

def facecut(im_name):  
    facedata = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(facedata)

    nim = cv2.imread(im_name)

    minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    faces = cascade.detectMultiScale(miniframe)

    for f in faces:
        x, y, wid, hei = [ v for v in f ]
        cv2.rectangle(img, (x,y), (x+wid,y+hei), (255,255,255))

        s_face = img[y:y+h, x:x+w]
        new_file = im_name+"-face" + ".png"
        cv2.imwrite(new_file, s_face)

		
			
		
