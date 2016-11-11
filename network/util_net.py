import numpy as np
import matplotlib.pyplot as plt

import caffe
from caffe.io import caffe_pb2,blobproto_to_array,Transformer

def loadMean(meanFile):
	fp = open(meanFile,'rb')
	proto_data = fp.read()
	fp.close()

	mean_blob = caffe_pb2.BlobProto()
	mean_blob.ParseFromString(proto_data)

	return blobproto_to_array(mean_blob)[0]

def loadNet1(deployFile, modelFile, meanFile):
	mean_array = loadMean(meanFile)

	net = caffe.Net(deployFile,modelFile,caffe.TEST)

	transformer = Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_mean('data', mean_array)
	transformer.set_transpose('data', (2,0,1))

	return net, transformer

def loadNet2(deployFile, modelFile, meanFile, imageWidth, imageHeight, visualize=True):
	mean_array = loadMean(meanFile)

	net = caffe.Classifier(deployFile,modelFile,
		mean=mean_array,
		channel_swap=(2,1,0),
		raw_scale=255,
		image_dims=(imageWidth,imageHeight))

	if visualize:
		transformer = Transformer({'data': net.blobs['data'].data.shape})
		transformer.set_transpose('data', (2,0,1))

		return net, transformer
	else:
		return net

# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, padsize=1, padval=0, visualize=False):
	print data.min(), data.max()

	data -= data.min()
	data /= data.max()

	# force the number of filters to be square
	n = int(np.ceil(np.sqrt(data.shape[0])))
	padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
	data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

	# tile the filters into an image
	data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
	data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

	plt.imshow(data)
	if visualize:
		plt.show()