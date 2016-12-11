import glob
import os

from constantes import *

def deleteImagenes(imagenes):
	for imagen in imagenes:
		os.remove(imagen)

def main():
	carpetas = glob.glob(RUTA + AUGMENTATION_PATH + '/*')
	#carpetas = [RUTA + '/augmentation/atun']

	for carpeta in carpetas:
		carpeta = os.path.abspath(carpeta)

		print carpeta

		if not os.path.isdir(carpeta):
			continue

		imagenes = glob.glob(carpeta + '/*.jpeg')	

		deleteImagenes(imagenes[VOLUMEN:])

if __name__ == '__main__':
	main()