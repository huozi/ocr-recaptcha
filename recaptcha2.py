#! usr/bin/env python
# -*- coding: utf-8 -*-

#filename recaptcha2.py

from PIL import Image
from PIL import ImageFilter
import requests


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"
## verification code address
pic_url = "http://www.example.com/user/authcode.do"


def get_img():

	s = requests.Session()
	r = s.get(url=pic_url, headers={'User-Agent' : UA})
	raw = r.content
	#print raw
	with open("./image2/tmp.jpg", 'wb') as fp:
		fp.write(raw)

	return Image.open("./image2/tmp.jpg")


def ocr_question_extract(im):
	# git@github.com:madmaze/pytesseract.git
	global pytesseract
	try:
		import pytesseract
	except:
		print "[ERROR] pytesseract not installed"
		return
	im = pre_ocr_processing(im)
	#output median value
	im.save("./image2/tmp1.jpg")
	
	return pytesseract.image_to_string(im).strip()

def pre_ocr_processing(im):
	im = im.convert("RGB")
	width, height = im.size
	white = im.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(23))
	
	grey = im.convert('L')
	impix = im.load()
	whitepix = white.load()
	greypix = grey.load()

	for y in range(height):
		for x in range(width):
			greypix[x,y] = min(255, max(255 + impix[x,y][0] - whitepix[x,y][0],
				255 + impix[x,y][1] - whitepix[x,y][1],
				255 + impix[x,y][2] - whitepix[x,y][2]))

	new_im = grey.copy()
	new_im.save('./image2/before_binarize.jpg')
	binarize(new_im, 150)
	new_im.save('./image2/after_binarize.jpg')
	return new_im


def binarize(im, thresh=120):
	assert 0 < thresh < 255
	assert im.mode == 'L'
	w, h = im.size
	for y in xrange(0, h):
		for x in xrange(0, w):
			if im.getpixel((x,y)) < thresh:
				im.putpixel((x,y), 0)
			else:
				im.putpixel((x,y), 255)


if __name__ == '__main__':
	for i in range(10):
		im = Image.open("./image2/tmp_"  + str(i) + ".jpg")
		print 'OCR Code:', ocr_question_extract(im)