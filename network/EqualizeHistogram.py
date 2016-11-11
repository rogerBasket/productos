from PIL import Image
import numpy as np
import math

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
		if len(args) == PARAMETROS_RGB:
			espacio = []

			for i in args[1]:
				pixel = np.array(i).reshape((3,1))
				iluminacion = np.dot(RGB_YCBCR_MATRIZ,pixel)+RGB_YCBCR

				espacio.append(tuple(iluminacion.reshape(CANALES_RGB)))
			
			print espacio[args[3]], args[1][args[3]]

		return funcion(*args)

	return wrapper

def yCbCrToRgb(self, iluminacion):
	print iluminacion
	pixel = np.dot(YCBCR_RGB_MATRIZ,iluminacion.reshape((3,1))-RGB_YCBCR).reshape(3)
	return (int(pixel[0]),int(pixel[1]),int(pixel[2]))

# probability mass function
def pmf(self, funcion, histogram):
	result = []

	#histogram = range(10)

	if histogram != None and isinstance(histogram,list):
		total = len(histogram)
		#print total

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

@rgbToYCbCr
def equalized(self, canal, cdf, band = None):
	eh = []

	valMin = min(cdf, key=lambda x: x if x > 0 else np.inf)
	n = self.width*self.height

	#print 'len cdf:', len(cdf), len(canal), valMin

	try:
		if band == None:
			for i in canal:
				#eh.append(int(math.ceil((float(cdf[i]-valMin)/float(n-valMin))*ESCALA)))
				value = (float(cdf[int(i)]-valMin)/float(n-valMin))*ESCALA
				if value - 0.5 >= int(value):
					eh.append(int(math.ceil(value)))
				else:
					eh.append(int(math.floor(value)))
		else:
			for i in canal:
				#print i
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
		self.histogram = imagen.histogram()
		self.imagen = imagen

	def start(self):
		newImage = Image.new(self.imagen.mode,self.imagen.size)
		newHistogram = []

		if self.imagen.mode == 'L':
			sumatoria = self.pmf(self.cdf,self.histogram)
			newHistogram = self.equalized(list(self.imagen.getdata()),sumatoria)
		elif self.imagen.mode == 'RGB':
			#print len(self.histogram)

			sumR = self.pmf(self.cdf,self.histogram[:RANGO_RGB])
			sumG = self.pmf(self.cdf,self.histogram[RANGO_RGB:2*RANGO_RGB])
			sumB = self.pmf(self.cdf,self.histogram[2*RANGO_RGB:])

			histR = self.equalized(list(self.imagen.getdata()),sumR,0)
			if histR != None:
				histG = self.equalized(list(self.imagen.getdata()),sumG,1)
				if histG != None:
					histB = self.equalized(list(self.imagen.getdata()),sumB,2)					
					if histB != None:
						for i in range(self.width*self.height):
							pixel = self.yCbCrToRgb(np.array((histR[i],histG[i],histB[i])))
							print pixel
							newHistogram.append(pixel)
							break
					else:
						print 'error en imagen:', self.imagen,
						print 'canal b'
				else:
					print 'error en imagen:', self.imagen,
					print 'canal g'
			else:
				print 'error en imagen:', self.imagen,
				print 'canal r'

		newImage.putdata(newHistogram)
		#print np.array(newHistogram).reshape(8,8)

		return newImage

	cdf = cdf
	pmf = pmf
	equalized = equalized
	yCbCrToRgb = yCbCrToRgb


#im = Image.open('unequalized.jpg')
im = Image.open('hershey.jpg')
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


#newImage.save('equalized.jpg')

fp.close()