#coding=utf-8 

import glob
import os
import lmdb
import random
import numpy as np
import math

from PIL import Image

from caffe.io import array_to_datum

from groups_mongo import getClassAndName
from EqualizeHistogram import EqualizeHistogram

RUTA = '/home/roger/caffe-productos'
SCORE = 6

def createDB(name, imagenes, clase, funcion):
	db = lmdb.Environment(name, map_size=int(1e12))
	tx = db.begin(write=True)
	punt = None

	for label, imagen in enumerate(imagenes):
		try:
			if funcion(label,SCORE):
				im = Image.open(imagen)
				punt = im.fp

				if im.mode != 'RGB':
					im = im.convert('RGB')

				'''	
				eh = EqualizeHistogram(im)
				newImage = eh.start()
				newImage = newImage.resize((IMAGE_WIDTH,IMAGE_HEIGHT))

				#print imagen, newImage.size, newImage.mode
					
				x = np.array(newImage.getdata()).reshape(newImage.size[1],newImage.size[0],3)
				'''

				x = np.array(im.getdata()).reshape(im.size[1],im.size[0],3)
				datum = array_to_datum(np.transpose(x,(2,0,1)),clase)

				print label
				tx.put('{:08}'.format(label),datum.SerializeToString())
		
			if (label+1) % 50 == 0:
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
	db.close()

def main():
	if os.path.exists(RUTA):
		carpetas = glob.glob(os.path.abspath(RUTA)+'/images/*')
		clases = getClassAndName()

		for carpeta in carpetas:
			if not os.path.isdir(os.path.abspath(carpeta)):
				print 'ruta encontrada no es un directorio: ' + str(carpeta)
				continue

			clave = os.path.basename(carpeta)

			'''
			if clave in ['cafe','cigarros','galletas','catsup','pañales',
				'talco','sal','chocolate','cajeta','atun','mostaza']:
				continue
			'''

			for i in clases:
				if i['nombre'].encode('utf-8') == clave:
					#print clave, i['clase']
					clase = i['clase']
					break

			print clase, clave

			imagenes = glob.glob(os.path.abspath(carpeta)+'/*.jpg')
			#imagenes = [os.path.abspath(carpeta)+'/cafe1062.jpg']

			random.shuffle(imagenes)

			print 'Creando lmdb train'
			createDB(os.path.abspath(RUTA) + '/train_lmdb',imagenes,clase,lambda x, y: x % y != 0) # lmdb train
			print 'Done.'

			print 'Creando lmdb validation'
			createDB(os.path.abspath(RUTA) + '/validation_lmdb',imagenes,clase,lambda x, y: x % y == 0) # lmdb validation
			print 'Done.'

		#print clases

if __name__ == '__main__':
	main()