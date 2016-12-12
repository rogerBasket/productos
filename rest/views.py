from django.shortcuts import render
from django.core.urlresolvers import reverse

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .response import JSONResponse, response_mimetype
from .constantes import *

import utils

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

	def post(self, request, filename):
		print 'ClassificationImage - post'

		return JSONResponse({'ok': 1})

def index(request):
	if not utils.reset():
		return JSONResponse({'error': 'Error en el directorio "tmp" del servidor'})

	return render(request, 'rest/' + PLUGIN_UPLOAD_IMAGES + '/angularjs.html', {})
