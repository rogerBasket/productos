from PIL import Image
import numpy as np
import math
import sys

ESCALA = 255
CANALES_RGB = 3
RANGO_RGB = 256

PARAMETROS_RGB = 4

RGB_YCBCR = np.array([[0],[128],[128]])
RGB_YCBCR_MATRIZ = np.array([
	[0.299,0.587,0.114],
	[-0.169,-0.331,0.500],
	[0.500,-0.419,-0.081]
])

YCBCR_RGB_MATRIZ = np.array([
	[1.000,0.000,1.400],
	[1.000,-0.343,-0.711],
	[1.000,1.765,0.000]
])

def rgbToYCbCr(funcion):

	def wrapper(*args, **kargs):
		if args[0].imagen.mode == 'RGB':
			espacio = []

			data = args[0].imagen.getdata()

			for i in data:
				pixel = np.array(i).reshape((3,1))
				iluminacion = np.dot(RGB_YCBCR_MATRIZ,pixel)+RGB_YCBCR

				conversion = iluminacion.reshape(CANALES_RGB)

				Y = max(0,min(int(conversion[0]),ESCALA))
				Cb = max(0,min(int(conversion[1]),ESCALA))
				Cr = max(0,min(int(conversion[2]),ESCALA))

				espacio.append((Y,Cb,Cr))
			
			im = Image.new('YCbCr',args[0].imagen.size)	
			im.putdata(espacio)

			return funcion(args[0],espacio,im.histogram())
		else:
			return funcion(*args)

	return wrapper

def yCbCrToRgb(self, iluminacion):
	pixel = np.dot(YCBCR_RGB_MATRIZ,iluminacion.reshape((3,1))-RGB_YCBCR).reshape(3)

	r = max(0,min(int(pixel[0]),ESCALA))
	g = max(0,min(int(pixel[1]),ESCALA))
	b = max(0,min(int(pixel[2]),ESCALA))

	#print iluminacion,pixel,(r,g,b)

	return (r,g,b)

def calculateHistogram(self, data):
	histogram = np.zeros((RANGO_RGB),dtype=int)

	for i in range(len(histogram)):
		histogram[data[i][0]] += 1

	return histogram

# probability mass function
def pmf(self, funcion, histogram):
	result = []

	if histogram != None and isinstance(histogram,list):
		total = len(histogram)

		for i in histogram:
			#result.append(i/float(total))
			result.append(i)

	return funcion(result)

# cumulative distributive function
def cdf(self, pmf):
	sumatoria = []
	acumulado = 0

	for i in pmf:
		sumatoria.append(i+acumulado)
		acumulado += i

	return sumatoria

def equalized(self, canal, cdf, band = None):
	eh = []

	valMin = min(cdf, key=lambda x: x if x > 0 else np.inf)
	n = self.width*self.height

	try:
		if band == None:
			for i in canal:
				value = (float(cdf[int(i)]-valMin)/float(n-valMin))*ESCALA
				if value - 0.5 >= int(value):
					eh.append(int(math.ceil(value)))
				else:
					eh.append(int(math.floor(value)))
		else:
			for i in canal:
				value = (float(cdf[int(i[band])]-valMin)/float(n-valMin))*ESCALA
				if value - 0.5 >= int(value):
					eh.append(int(math.ceil(value)))
				else:
					eh.append(int(math.floor(value)))
	except ZeroDivisionError as zde:
		return None

	return eh

class EqualizeHistogram:

	def __init__(self, imagen):
		self.width, self.height = imagen.size
		self.imagen = imagen

	@rgbToYCbCr
	def start(self, data = None, histogram = None):

		#print histogram

		newImage = Image.new(self.imagen.mode,self.imagen.size)
		newHistogram = []

		if self.imagen.mode == 'L':
			sumatoria = self.pmf(self.cdf,self.imagen.histogram())
			newHistogram = self.equalized(list(self.imagen.getdata()),sumatoria)
		elif self.imagen.mode == 'RGB':
			sumatoria = self.pmf(self.cdf,histogram[:RANGO_RGB])
			equalizar = self.equalized(list(data),sumatoria,0)

			for i in range(self.width*self.height):
				pixel = self.yCbCrToRgb(np.array((equalizar[i],data[i][1],data[i][2])))
				newHistogram.append(pixel)

			'''
			sumR = self.pmf(self.cdf,histogram[:RANGO_RGB])
			sumG = self.pmf(self.cdf,histogram[RANGO_RGB:2*RANGO_RGB])
			sumB = self.pmf(self.cdf,histogram[2*RANGO_RGB:])

			histR = self.equalized(list(data),sumR,0)
			if histR != None:
				histG = self.equalized(list(data),sumG,1)
				if histG != None:
					histB = self.equalized(list(data),sumB,2)					
					if histB != None:
						for i in range(self.width*self.height):
							pixel = self.yCbCrToRgb(np.array((histR[i],histG[i],histB[i])))
							newHistogram.append(pixel)
					else:
						print 'error en imagen:', self.imagen,
						print 'canal b'
				else:
					print 'error en imagen:', self.imagen,
					print 'canal g'
			else:
				print 'error en imagen:', self.imagen,
				print 'canal r'
			'''

		newImage.putdata(newHistogram)

		return newImage

	cdf = cdf
	pmf = pmf
	equalized = equalized
	yCbCrToRgb = yCbCrToRgb
	calculateHistogram = calculateHistogram

if __name__ == '__main__':
	im = Image.open(sys.argv[1])
	fp = im.fp
	print im.mode, im.size


	'''
	datos = [52,55,61,66,70,61,64,73,
			63,59,55,90,109,85,69,72,
			62,59,68,113,144,104,66,73,
			63,58,71,122,154,106,70,69,
			67,61,68,104,126,88,68,70,
			79,65,60,70,77,68,58,75,
			85,71,64,59,55,61,65,83,
			87,79,69,68,65,76,78,94]

	im = Image.new('L',(8,8))
	im.putdata(datos)
	'''


	eh = EqualizeHistogram(im)
	newImage = eh.start()
	#print np.array(list(newImage.getdata())).reshape(8,8)


	newImage.save('eq-'+sys.argv[1])

	fp.close()