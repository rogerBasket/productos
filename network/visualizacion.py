import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from util_net import vis_square, loadNet2
from constantes import *

import warnings
warnings.filterwarnings("error")

def main():
	imagenAleatoria = np.random.random((1,3,227,227))
	label = np.zeros((1,2,1,1))

	net = loadNet2(DEPLOY_FILE,MODEL_FILE,
		MEAN_FILE,IMAGE_WIDTH,IMAGE_HEIGHT,False)

	i = 0
	while i < 1000:
		try:
			out = net.forward(data = imagenAleatoria)

			bw = net.backward()
			diff = bw['data']
			#diff = net.blobs['data'].data

			imagenAleatoria = np.array(imagenAleatoria, dtype = float)
			imagenAleatoria += 0.01*diff
			print i
			i += 1
		except RuntimeWarning:
			break

	params = {'visualize': True}

	vis_square(imagenAleatoria.transpose(0,2,3,1),**params)
	plt.savefig('ps3part1.png')

if __name__ == '__main__':
	main()