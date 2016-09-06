import json
from pymongo import MongoClient
 
from googleapiclient.discovery import build

from urls_mongo import getTotalResults
from search_mongo import getDocumentByCategoria

RESPUESTAS = 10
IMAGES = 10

def getKeys(properties):
	f = open(properties,'r')
	val = []
	for linea in f:
		if linea[-1] == '\n':
			linea = linea[:-1]
		val.append(linea)

	f.close()

	return val

# funcion generadora del numero de peticiones
def peticiones():
	n = 1
	while n < IMAGES:
		yield n
		n = n+RESPUESTAS

def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	global IMAGES

	try:
		#developer_key, custom_search_id = getKeys('google_api_dev.prop')
		developer_key, custom_search_id = getKeys('google_api_prod.prop')
	except:
		print 'parametros del archivo incorrectos'
		exit()

	print developer_key, custom_search_id

	service = build("customsearch", "v1",
		developerKey=developer_key.split('=')[1])

	#creacion de instancia con MongoDB
	client = MongoClient()
	db = client.google_images
	search = db.search
	urls = db.urls

	productos = getDocumentByCategoria(search,'refresco').next()
	
	'''
	print len(productos['descripcion'][0]['busqueda'])
	print json.dumps(productos,indent=4,separators=(';',':'))
	'''
	
	for i in [productos['descripcion'][0]]:
		for j in [i['busqueda'][0]]:
			flag = True
			#print j, type(j)
			for k in peticiones():

				webService = service.cse().list(
					q='nike',
					cx=custom_search_id.split('=')[1],
					filter='1',
					searchType='image',
					num=RESPUESTAS,
					start=k)

				#print webService.to_json()
				urlsImages = webService.execute()
				urlsImages['categoria'] = productos['categoria']
				urlsImages['descripcion'] = i['nombre']

				urlsJson = json.dumps(urlsImages,indent=4,separators=(',',':'))
	
				#print urlsJson
				#print type(urlsImages), type(urlsJson)

				urls.insert(urlsImages)

				if flag:
					totalResults = getTotalResults(urls)
					#print int(totalResults)
					if totalResults < IMAGES:
						IMAGES = totalResults
					flag = False

if __name__ == '__main__':
	main()
	