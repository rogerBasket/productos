import numpy as np

import glob
from PIL import Image

from util_net import loadNet1, loadNet2

class Clasificacion:

	def __init__(self, ruta = '.', ancho = 256, alto = 256, deploy = None, model = None, mean = None):
		if model == None or deploy == None or mean == None:
			raise Exception('datos insuficientes para clasificacion')
			
		self.__ruta = ruta
		self.__ancho = ancho
		self.__alto = alto
		self.__model = model
		self.__deploy = deploy
		self.__mean = mean

	def start(self):
		imagenes = glob.glob(self.__ruta + '/*.jpg')
		aleatorio = np.random.randint(len(imagenes))
		imagen = imagenes[aleatorio]
		
		print imagen

		#self.__net, self.__transformer = loadNet1(self.__deploy,self.__model,self.__mean)
		self.__net, self.__transformer = loadNet2(self.__deploy,self.__model,self.__mean,self.__ancho,self.__alto)

		input_image = Image.open(imagen)
		fp = input_image.fp
		input_image = input_image.resize((self.__ancho,self.__alto))
		input_image = np.array(input_image.getdata()).reshape(input_image.size[1],input_image.size[0],3)
		fp.close()

		self.__net.blobs['data'].data[...] = self.__transformer.preprocess('data',input_image)
		self.__out = self.__net.forward()
		self.imagen = imagen
		
	def getNet(self):
		return self.__net

	def getOut(self):
		return self.__out

	def getTransformer(self):
		return self.__transformer