import os
import glob
from PIL import Image
from EqualizeHistogram import EqualizeHistogram

class CreateAllHistogram:
	RUTA = '/home/roger/caffe-productos'	
	IMAGE_WIDTH = 227
	IMAGE_HEIGHT = 227

	def __init__(self):
		self.ruta = CreateAllHistogram.RUTA
		self.width = CreateAllHistogram.IMAGE_WIDTH
		self.height = CreateAllHistogram.IMAGE_HEIGHT

	def start(self):
		carpetas = glob.glob(os.path.abspath(self.ruta)+'/images/*')

		for carpeta in carpetas:

			if os.path.basename(carpeta) in ['cafe']:
				continue

			if not os.path.isdir(os.path.abspath(carpeta)):
				print 'ruta encontrada no es un directorio: ' + str(carpeta)
				continue

			imagenes = glob.glob(os.path.abspath(carpeta)+'/*.jpg')

			nuevaRuta = self.ruta+'/histogram/'+os.path.basename(carpeta)
			if not os.path.exists(nuevaRuta):
				os.makedirs(nuevaRuta)

			for imagen in imagenes:
				punt = None

				try:
					im = Image.open(imagen)
					punt = im.fp

					eh = EqualizeHistogram(im)
					newImage = eh.start()
					newImage = newImage.resize((self.width,self.height))

					#print imagen

					newImage.save(nuevaRuta+'/'+os.path.basename(imagen))
				except IOError as ioe:
					print 'Imagen:', imagen
					print ioe
				finally:
					if punt != None and not punt.closed:
						punt.close()

			print carpeta

c = CreateAllHistogram()
c.start()