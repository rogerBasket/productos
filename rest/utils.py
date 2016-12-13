from .constantes import *

import glob
import re
import os

def createImage(file, image):
	print 'createImage', image

	flag = True
	size = 0

	try:
		f = open(PATH_SERVER + STATIC_PATH_SERVER + TEMP + str(image),'wb+')

		for i in file.chunks():
			f.write(i)

		size = f.tell()

		f.close()
	except IOError as ioe:
		print ioe
		flag = False

	return flag, size

def deleteImage(image):
	print 'deleteImage', image

	flag = True

	try:
		ruta = PATH_SERVER + STATIC_PATH_SERVER + TEMP + image

		if os.path.exists(ruta):
			os.remove(os.path.abspath(ruta))
		else:
			raise IOError('No existe imagen en el servidor ' + image)
	except IOError as ioe:
		print ioe
		flag = False

	return flag

def listImages():
	print 'listImages'

	imagenes = glob.glob(PATH_SERVER + STATIC_PATH_SERVER +  TEMP + '*')
	coinciden = []

	regex = re.compile(r'' + REGEX_IMAGES)

	for i in imagenes:
		filename = os.path.basename(i)
		if regex.match(filename):
			coinciden.append(filename)

	return coinciden

def lenImage(image):
	return os.stat(PATH_SERVER + STATIC_PATH_SERVER + TEMP + image).st_size

def reset():
	flag = True

	if os.path.exists(os.path.abspath(PATH_SERVER + STATIC_PATH_SERVER + TEMP)):
		archivos = glob.glob(PATH_SERVER + STATIC_PATH_SERVER + TEMP + '*')

		try:
			for archivo in archivos:
				os.remove(os.path.abspath(archivo))
		except OSError as ose:
			print ose
			flag = False
	else:
		os.makedirs(os.path.abspath(PATH_SERVER + STATIC_PATH_SERVER + TEMP))
	
	return flag