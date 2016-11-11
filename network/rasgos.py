import numpy as np
import matplotlib.pyplot as plt

from ClasificacionSingleton import utilitiesClassification as clasificacion

def main():
	net, out, transformer = clasificacion()

	diff = net.blobs['data'].data
	diff -= diff.min()
	diff /= diff.max()
	diff_sq = np.squeeze(diff)
	rasgos = np.amax(diff_sq,axis = 0)

	#print net.blobs['conv1'].data.min(), net.blobs['conv1'].data.max()

	plt.subplot(1,2,1)
	plt.imshow(rasgos)
	plt.subplot(1,2,2)
	plt.imshow(transformer.deprocess('data', net.blobs['data'].data[0]))
	plt.show()

if __name__ == '__main__':
	main()