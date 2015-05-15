#! /usr/bin/env python
# -*- coding: utf-8 -*-

# filename: recaptcha1.py

from PIL import Image
import urllib
from numpy import *

# verification code address
pic_url = "http://www.example.com/validateCode.do"


def get_img():
	resp = urllib.urlopen(pic_url)
	raw = resp.read()
	with open("./image1/tmp.jpg", 'wb') as fp:
		fp.write(raw)

	return Image.open("./image1/tmp.jpg")


def cmp(im, i, j, a, b, width, height):
	flg = False
	if a>=0 and b >= 0 and a<height and b<width and im[i,j]==0:
		if math.fabs(int(im[i, j]) - int(im[a, b]) )< 50 :
			flg = True
	return flg

def remove_spot(im):
	width, height = im.size
	# output median value
	im.convert('L').save('./image1/tmp1.jpg')

	# binarization image
	im = array(im.convert('L'))
	for i in range(height):
		for j in range(width):
			if im[i, j] >150:
				im[i, j] = 255
			else:
				im[i, j] = 0
	
	# output median value
	img = Image.fromarray(im, 'L')
	img.save('./image1/tmp2.png')

	#clean image 
	for i in range(height):
		for j in range(width):
			num = 0
			if cmp(im, i, j, i-1, j-1, width, height):
				num += 1
			if cmp(im, i, j, i, j-1, width, height):
				num += 1
			if cmp(im, i, j, i+1, j-1, width, height):
				num += 1
			if cmp(im, i, j, i-1, j, width, height):
				num += 1
			if cmp(im, i, j, i+1, j, width, height):
				num += 1
			if cmp(im, i, j, i-1, j+1, width, height):
				num += 1
			if cmp(im, i, j, i, j+1, width, height):
				num += 1
			if cmp(im, i, j, i+1, j+1, width, height):
				num += 1
			if num <= 3 :
				im[i, j] = 255
	# output median value
	img = Image.fromarray(im, 'L')
	img.save('./image1/tmp3.png')

	return img


def ocr_recaptcha(im):
	# git@github.com:madmaze/pytesseract.git
	global pytesseract
	try:
		import pytesseract
	except:
		print "[ERROR] pytesseract is not installed"
		return
	im = remove_spot(im)
	return pytesseract.image_to_string(im).strip()


if __name__ == '__main__':
	# im = get_img()
	# print 'OCR Code:', ocr_recaptcha(im)
	for i in range(10):
		im = Image.open("./image1/tmp_" + str(i) + ".jpg")
		print 'OCR Code:', ocr_recaptcha(im)