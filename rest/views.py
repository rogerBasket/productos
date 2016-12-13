from django.shortcuts import render
from django.core.urlresolvers import reverse

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .response import JSONResponse, response_mimetype, response_classification
from .ServerException import ServerException
from .constantes_service import *
from .constantes_network import LEARN
from .SingletonLabels import *
from . import network
from . import utils

import sys
import time


formato = {
	'jpg': 'image/jpg',
	'jpeg': 'image/jpg',
	'png': 'image/png'
}

response_json = {
	'url': None,
	'name': None,
	'type': None,
	'thumbnailUrl': None,
	'size': None, 
	'deleteUrl': None,
	'deleteType': 'DELETE',
}

class SingleImage(APIView):

	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, format = None):	
		print 'SingleImage - POST'

		file = request.data['file']
		image = str(file)
		sufijo = image.split('.')[1]

		flag, size = utils.createImage(file,image)

		if not flag:
			return JSONResponse({'error': 'Error al crear imagen en el servidor'})

		response_json['url'] = '/' + STATIC_PATH_SERVER + TEMP + image
		response_json['name'] = image
		response_json['type'] = formato[sufijo]
		response_json['thumbnailUrl'] = '/' + STATIC_PATH_SERVER + TEMP + image
		response_json['size'] = size
		response_json['deleteUrl'] = reverse('delete-image', kwargs = {'filename': image})

		data = {
			'files': [response_json]
		}
			
		response = JSONResponse(data, mimetype = response_mimetype(request))

		return response

class DeleteImage(APIView):

	def delete(self, request, *args, **kwargs):
		print 'DeleteImage - delete'
		
		filename = kwargs['filename']

		if not utils.deleteImage(filename):
			return JSONResponse({'error': 'Error al eliminar imagen en el servidor'})

		images = utils.listImages()

		listImages = []
		for i in images:
			sufijo = i.split('.')[1]
			resp = dict(response_json)

			resp['url'] = '/' + STATIC_PATH_SERVER + TEMP + i
			resp['name'] = i
			resp['type'] = formato[sufijo]
			resp['thumbnailUrl'] = '/' + STATIC_PATH_SERVER + TEMP + i
			resp['size'] = utils.lenImage(i)
			resp['deleteUrl'] = reverse('delete-image', kwargs = {'filename': i})

			listImages.append(resp)

		#print listImages

		return JSONResponse({'files': listImages}, mimetype = response_mimetype(request))

class ClassificationImage(APIView):

	def post(self, request, filename, format = None):
		print 'ClassificationImage - post'

		try:
			inicio = time.time()

			prob = network.prediction(filename)

			'''
			if prob == None:
				raise ServerException('error al clasificar la imagen: ' + filename)
			'''

			labels = getLabels()
		
			return JSONResponse({
					'tiempo': time.time() - inicio,
					'multiple': [response_classification(prob,labels,filename)]
				})
		except:
			print 'excepcion no controlada en el servidor', sys.exc_info()
			raise

class MultipleClassification(APIView):

	def post(self, request, format = None):
		print 'MultipleClassificationImage - post'

		#print request.data

		try:
			listFiles = []
			for i in request.data:
				listFiles.append(i.encode('utf-8'))

			inicio = time.time()

			probs = network.multiplePredictions(listFiles)

			labels = getLabels()

			multiple_resp = []
			for prob, filename in zip(probs,listFiles):
				print prob.argmax(), labels[prob.argmax()]
				
				multiple_resp.append(response_classification(prob,labels,filename))

			return JSONResponse({
					'tiempo': time.time() - inicio,
					'multiple': multiple_resp
				})
		except:
			print 'excepcion no controlado en el servidor', sys.exc_info()
			raise

class LearningImage(APIView):

	def post(self, request, filename, format = None):
		print 'LearningImage - post'

		#print request.data

		try:
			dataLayers = []
			for i in request.data:
				dataLayers.append(i.encode('utf-8'))

			inicio = time.time()

			features, prob = network.backpropagation(filename,dataLayers)

			labels = getLabels()

			learning = []
			for i, j in zip(dataLayers,features):
				learning.append({
						'layer': i,
						'url': '/' + STATIC_PATH_SERVER + LEARN + j,
						'thumbnailUrl': '/' + STATIC_PATH_SERVER + LEARN + j
					})

			return JSONResponse({
					'id': 'learning',
					'imagen': filename,
					'clase': labels[prob.argmax()],
					'url': '/' + STATIC_PATH_SERVER + TEMP + filename,
					'thumbnailUrl': '/' + STATIC_PATH_SERVER + TEMP + filename,
					'tiempo': time.time() - inicio,
					'learning': learning
				})
		except:
			print 'excepcion no contralado en el servidor', sys.exc_info()
			raise

def index(request):
	if not utils.reset():
		return JSONResponse({'error': 'Error en el directorio "tmp" del servidor'})

	return render(request, 'rest/angularjs.html', {})
