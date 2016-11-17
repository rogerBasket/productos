import matplotlib.pyplot as plt

from ClasificacionSingleton import utilitiesClassification as clasificacion, \
	getImagen 
from util_net import vis_square

def main():
	net, out, transformer = clasificacion()
	
	print getImagen(), out['prob'].argmax()

	'''
	top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-3:-1]
	print top_k

	for i in range(cnt.CAPAS):
	    print 'probabilidad: ',net.blobs['prob'].data[0].flatten()[top_k[i]]

	print 'suma de probabilidades: ',str(sum(net.blobs['prob'].data[0].flatten()))
	'''

	print 'Conv1'
	feat = net.blobs['conv1'].data[0, :256]
	#vis_square(feat, padval=0.5)
	vis_square(feat, padval=1)
	plt.title('conv1')
	plt.savefig('backpropagation_conv1.png')

if __name__ == '__main__':
	main()