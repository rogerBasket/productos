import json
import time
#from pymongo import MongoClient
 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from urls_mongo import getTotalResults, getFindCategoria, \
deleteUrlsByCategoria, getCountDocumentsByCategoria, addDocumentInUrls, \
getTotalDocumentsUrls
from search_mongo import getDocumentByCategoria, getTotalResultsByCategoria
from groups_mongo import getAllCategoria

RESPUESTAS = 10
IMAGES = 100
PORCENTAJE = int(IMAGES/RESPUESTAS)
RESET = False
INTENTOS = 10

def getKeys(properties):
	f = open(properties,'r')
	val = []
	for linea in f:
		if linea[-1] == '\n':
			linea = linea[:-1]
		val.append(linea)

	f.close()

	return val

def count():
	count.var += 1

count.var = 0

# funcion generadora del numero de peticiones
def peticiones():
	global RESET

	n = 1
	while n < IMAGES:
		yield n
		if not RESET:
			n += RESPUESTAS
		else:
			count()
		RESET = False

	#time.sleep(1)

# obtener las categorias que se encuentran en la collection urls
def listaCategoriasInUrls(categoriasGroups):
	categoriasUrls = []

	for i in categoriasGroups:
		print i['nombre']
		categoriaUrls = getFindCategoria(i['nombre'])
		
		if categoriaUrls != None:
			categoriasUrls.append(categoriaUrls)

	return categoriasUrls

def totalQueryByCategoria(categoria):
	results = getTotalResultsByCategoria(categoria)
	total = 0

	if results != None:
		for i in results:
			total += len(i['busqueda'])

	return total

def matchingTotalByCategoria(categoria):
	totalSearch = totalQueryByCategoria(categoria)*PORCENTAJE
	totalUrls = getCountDocumentsByCategoria(categoria)

	#print totalSearch, totalUrls

	if totalSearch != totalUrls:
		deleteUrlsByCategoria(categoria)
		return False

	return True

def totalDocuments(categoriasGroups):
	total = 0

	for i in categoriasGroups:
		total += totalQueryByCategoria(i)*PORCENTAJE

	return total

def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	global IMAGES
	global RESET

	try:
		#developer_key, custom_search_id = getKeys('google_api_dev.prop')
		developer_key, custom_search_id = getKeys('google_api_prod.prop')
	except:
		print 'parametros del archivo incorrectos'
		exit()

	print developer_key
	print custom_search_id

	service = build("customsearch", "v1",
		developerKey=developer_key.split('=')[1])

	categoriasGroups = getAllCategoria()
	categoriasUrls = listaCategoriasInUrls(categoriasGroups)

	for i in categoriasUrls:
		if not matchingTotalByCategoria(i):
			categoriasUrls.remove(i)
	
	print 'total de documentos: ' + str(totalDocuments(categoriasGroups))

	'''
	for i in categorias['categoria']:
		print i.encode('utf-8'), type(i.encode('utf-8'))
	'''
	
	'''
	print len(productos['descripcion'][0]['busqueda'])
	print json.dumps(productos,indent=4,separators=(';',':'))
	'''

	for categoria in categoriasGroups:
		if categoria['nombre'] not in categoriasUrls:
			productos = getDocumentByCategoria(categoria['nombre'])
			for descripcion in [productos['descripcion']]:
				for producto in descripcion:
					print '\n', producto['nombre'] + ':',

					for busqueda in [producto['busqueda']]:
						flag = True
						for patron in busqueda:
							print patron,

							for num in peticiones():
								webService = service.cse().list(
									q=patron.encode('utf-8'),
									cx=custom_search_id.split('=')[1],
									filter='1',
									searchType='image',
									num=RESPUESTAS,
									start=num)

								#print webService.to_json()
								try:
									urlsImages = webService.execute()
									count.var = 0
								except HttpError as he:
									print he, he.resp.status
									print 'categoria: ' + categoria['nombre']

									if count.var < INTENTOS:
										RESET = True
										time.sleep(5)
										continue
									else:
										print 'Servidor no responde'
										return

								urlsImages['categoria'] = productos['categoria']
								urlsImages['descripcion'] = producto['nombre']
								
								'''
								urlsJson = json.dumps(urlsImages,indent=4,separators=(',',':'))
								print urlsJson
								print type(urlsImages), type(urlsJson)
								'''

								addDocumentInUrls(urlsImages)

								if flag:
									totalResults = getTotalResults()
									#print int(totalResults)
									if totalResults < IMAGES:
										IMAGES = totalResults
									flag = False
									

	print 'total de documentos en collection urls: ' + str(getTotalDocumentsUrls())					

if __name__ == '__main__':
	main()
	