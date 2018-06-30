#!/usr/bin/env python 
#coding:utf-8
import pytesseract
from urllib.request import urlopen
import cv2 as cv
#from StringIO import StringIO
import numpy as np
from PIL import Image

def process_image(url=None,path=None):
    if url != None:
        image = url_to_image(url)
    elif path != None:
        image = cv.imread(path)
    else:
        return "Wrong Wrong Wrong, What are you doing ??? "

    print(url)
    gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    ret2,th2 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    dst = cv.fastNlMeansDenoising(th2,10,10,7)
    cv.imwrite('./uploads/tmp.jpg',dst)
    cao = Image.open('./uploads/tmp.jpg')
    print ("Recongizeing...")
    rec_string =  pytesseract.image_to_string(cao,lang='ind')
    print ("the result is {}".format(rec_string))
    return rec_string

def url_to_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image

