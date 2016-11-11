import glob
import os
import sys
from PIL import Image

RUTA = '/home/roger/caffe-productos/images'
MODOS = ['P','RGBA','LA']

def pngToJpg(carpeta = '.'):
	carpeta = os.path.abspath(carpeta)

	png = glob.glob(carpeta+"/*.png")
	for images in png:
		try: 
			i = Image.open(images) 
			fp = i.fp
			if i.mode in MODOS:
				i = i.convert('RGB')
			nombre, ext = os.path.splitext(os.path.basename(images))
			i.save(carpeta+'/'+nombre+'.jpg','jpeg')
			fp.close()
		except IOError as ioe:
			print carpeta, images
			print ioe

def depurar(carpeta = '.'):
	carpeta = os.path.abspath(carpeta)

	png = glob.glob(carpeta+'/*.png')

	for images in png:
		os.remove(images)

def renombrar(function, carpeta = '.'):
	carpeta = os.path.abspath(carpeta)
	nombre = os.path.basename(carpeta)

	imagenes = glob.glob(carpeta+'/*.jpg')

	for i,j in zip(imagenes,range(len(imagenes))):
		#print i
		function(i,carpeta,j)

def main(argv):
	carpetas = glob.glob(RUTA+'/*')
	#carpetas = ['cafe']

	for c in carpetas:
		if os.path.isdir(c):

			pngToJpg(c)
			depurar(c)
			if argv == 'test':
				renombrar(lambda x, y, z: os.rename(x,y+'/'+str(z)+'.jpg'),c)
			else:
				renombrar(lambda x, y, z: os.rename(x,y+'/'+os.path.basename(y)+str(z)+'.jpg'),c)

			#break

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] in ['test','train']:
			main(sys.argv[1])
		else:
			print 'argumentos invalidos, no se ejecuto el programa'
	else:
		print 'error al ejecutar el programa, ingrese argumentos'