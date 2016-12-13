import argparse
import os
import numpy as np
import glob
from PIL import Image

import caffe
from caffe.io import caffe_pb2, blobproto_to_array, Transformer

from constantes import *

import util_net

PIXEL_RANGE = 255

'''
def argumentos():
	parser = argparse.ArgumentParser(description = 'Predicciones de imagenes')

	parser.add_argument('-r', '--ruta', type=str, help='Ruta de imagenes TEST', required=True)

	args = parser.parse_args()

	return args.ruta

ruta = os.path.abspath(argumentos())

print ruta
'''

def normalizeRange(data, range):
	normalize = []

	matriz = np.ones(data.shape, dtype = np.float32)/PIXEL_RANGE

	return data*matriz

ruta = TEST_PATH

if os.path.exists(ruta):
	imagenes = glob.glob(ruta + '/' + '[0-1][0-9].jpg')

	net, transformer = util_net.loadNet2(DEPLOY_FILE,MODEL_FILE,MEAN_FILE,IMAGE_WIDTH,IMAGE_HEIGHT)

	labels = []
	predic = []

	multiple = []

	for n,i in enumerate(imagenes):
		print i
		multiple.append(caffe.io.load_image(i))

		#print multiple[n]

		img = Image.open(i)
		fp = img.fp
		#img = img.resize((IMAGE_WIDTH,IMAGE_HEIGHT))
		x = np.array(img.getdata(), dtype = np.float32).reshape(img.size[1],img.size[0],3)
		x = normalizeRange(x,PIXEL_RANGE)

		#print '----------------------'
		#print x

	a = net.predict(multiple)
	b = net.predict([x])

	print a, type(a), a.ndim, a.shape
	print b, type(b), b.ndim, b.shape

	for i in a:
		for j in i:
			print j