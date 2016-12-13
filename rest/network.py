import os
import glob

import numpy as np
import matplotlib.pyplot as plt

from .NormalizedImage import NormalizedImage
from .constantes_network import *
from .SingletonNet import *

RUTA = PATH_SERVER + STATIC_PATH_SERVER + LEARN

def normalizeRange(data):
	matriz = np.ones(data.shape, dtype = np.float32)/PIXEL_RANGE

	return data*matriz

def prediction(filename):
	print 'prediction'

	im = None

	try:
		net = getNet()
		transformer = getTransformer()

		normalizedImage = NormalizedImage(filename)
		im = normalizedImage.process()
		im = im.resize((IMAGE_WIDTH,IMAGE_HEIGHT))

		data = np.array(im.getdata(), dtype = np.float32).reshape(im.size[1],im.size[0],3)

		net.blobs['data'].data[...] = transformer.preprocess('data',data)

		out = net.forward()
		prob = out['prob']

		return prob.reshape(OUTPUTS)
	finally:
		if im != None:
			normalizedImage.close()

def multiplePredictions(listFiles):
	print 'multiplePredictions'

	net = getNet()
	multiple = []

	for filename in listFiles:
		im = None
		try:
			normalizedImage = NormalizedImage(filename)
			im = normalizedImage.process()

			data = np.array(im.getdata(), dtype = np.float32).reshape(im.size[1],im.size[0],3)
			data = normalizeRange(data)

			multiple.append(data)
		finally:
			if im != None:
				normalizedImage.close()

	return net.predict(multiple)

def backpropagation(filename, dataLayers = []):
	print 'backpropagation'

	prob = prediction(filename)

	net = getNet()

	features = []

	for conv in dataLayers:
		feat = net.blobs[conv].data[0, :256]
		#util_net.vis_square(feat, padval=0.5)
		util_net.vis_square(feat, padval=1)

		image = filename.split('.')[0] + '_backpropagation_' + conv + '.png'

		plt.title(conv)
		plt.axis('off')
		plt.savefig(RUTA + image)

		features.append(image)

	return features, prob
