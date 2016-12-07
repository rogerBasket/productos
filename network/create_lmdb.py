#coding=utf-8 

import glob
import os
import random
import numpy as np
import math

from PIL import Image

from caffe.io import array_to_datum

from EqualizeHistogram import EqualizeHistogram
from constantes import *
from SingletonLMDB import *

clase = -1
label = 0

productos = {
	'refresco' : 0,
	'yogur': 1,
	'boing': 2,
	'desodorante': 3,
	'papas': 4,
	'jabon': 5,
	'pasta dental': 6,
	'leche': 7,
	'chocolate': 8,
	'cereal': 9,
	'aceite cocina': 10,
	'aceite automovil': 11,
	'mermelada': 12,
	'mayonesa': 13,
	'catsup': 14,
	'mostaza': 15,
	'shampoo': 16,
	'talco': 17,
	'crema corporal': 18,
	'gel': 19,
	'pañales': 20,
	'crema': 21,
	'galletas': 22,
	'atun': 23,
	'palomitas': 24,
	'sal': 25,
	'cajeta': 26,
	'cafe': 27,
	'condones': 28,
	'cigarros': 29,
	'tequila': 30
}

def getImagesAndClases():
	carpetas = glob.glob(os.path.abspath(RUTA)+'/images/*')

	global clase

	for carpeta in carpetas:
		if not os.path.isdir(os.path.abspath(carpeta)):
			print 'ruta encontrada no es un directorio: ' + str(carpeta)
			continue

		clave = os.path.basename(carpeta)
		clase = productos[clave]		

		print clase, clave

		if clase == -1:
			exit(0)

		imagenes = glob.glob(os.path.abspath(carpeta)+'/*.jpg')

		random.shuffle(imagenes)

		yield imagenes

def getImagesFile():
	global clase

	clase = 11

	f = open('faltantes.txt','r')
	imagenes = []
	for linea in f:
		if linea[-1] == '\n':
			linea = linea[:-1]
		
		imagenes.append(linea)

	yield imagenes

def createDB(db, funcion):
	global label

	label = 0

	for imagenes in getImagesAndClases():
		tx = db.begin(write=True)
		punt = None

		for imagen in imagenes:
			try:
				label += 1

				if funcion(label,SCORE):
					im = Image.open(imagen)
					punt = im.fp
					im = im.resize((IMAGE_WIDTH,IMAGE_HEIGHT))

					if im.mode != 'RGB':
						im = im.convert('RGB')

					x = np.array(im.getdata()).reshape(im.size[1],im.size[0],3)
					datum = array_to_datum(np.transpose(x,(2,0,1)),clase)

					print label, imagen
					tx.put('{:08}'.format(label),datum.SerializeToString())
			
				if (label+1) % COMMIT == 0:
					tx.commit()
					tx = db.begin(write=True)
					print '------- commit -------'

			except IOError as ioe:
				print 'Imagen:', imagen
				print ioe
			except:
				pass
			finally:
				if punt != None and not punt.closed:
					punt.close()

		tx.commit()

def main():
	if os.path.exists(RUTA):
		
		print 'Creando lmdb train'
		createDB(getTrainDB(),lambda x, y: x % y != 0) # lmdb train
		print 'Done.'

		print 'Creando lmdb validation'
		createDB(getValidationDB(),lambda x, y: x % y == 0) # lmdb validation
		print 'Done.'

	closeTrain()
	closeValidation()

if __name__ == '__main__':
	main()
