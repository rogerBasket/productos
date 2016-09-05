import json
from pymongo import MongoClient
 
from googleapiclient.discovery import build

from urls_mongo import getTotalResults
from search_mongo import getDocumentByCategoria

RESPUESTAS = 10
IMAGES = 100

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
		developer_key, custom_search_id = getKeys('google_api_dev.prop')
		#developer_key, custom_search_id = getKeys('google_api_prod.prop')
	except:
		print 'parametros del archivo incorrectos'

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

	for i in productos['descripcion']:
		for j in i['busqueda']:
			flag = True
			for k in peticiones():
				#print j

				webService = service.cse().list(
					q=j,
					cx=custom_search_id.split('=')[1],
					filter='1',
					searchType='image',
					num=RESPUESTAS,
					start=k)

				#print webService.to_json()

				resp = webService.execute()

				if flag:
					totalResults = getTotalResults(search).next()
					print totalResults
					if totalResults < IMAGES:
						IMAGES = totalResults
					flag = False

	'''
		print search.insert(resp)
	'''

if __name__ == '__main__':
	main()
	