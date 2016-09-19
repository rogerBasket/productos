import urllib2
import os
from datetime import datetime
import socket

from Nodo import Nodo
from ABB import addNodo, inorden
from urls_mongo import *
from groups_mongo import getAllCategoria

formato = {
	'image/jpeg':'jpg',
	'image/png':'png'
}

RUTA = '/home/roger/caffe-productos/'

def main():
	if os.path.exists(RUTA):
		absoluta = os.path.abspath(RUTA)

	categoriasGroups = getAllCategoria()

	for categoria in categoriasGroups:
		if categoria in ['refresco','yogur','boing','desodorante','jabon',
			'papas','cereal','leche','aceite automovil','aceite cocina','chocolate'
			'catsup','pasta dental','mermelada','mayonesa']:
			continue

		if not os.path.exists(categoria):
			os.makedirs(absoluta + '/' + categoria)
		else:
			continue

		print 'categoria: ' + categoria

		urlsDocuments = getInfoUrlsByCategoria(categoria)

		first = getFirstByCategoria(categoria)
		if first != None:
			ext = first['mime']
			if formato.has_key(ext):
				raiz = Nodo(first['link'].encode('utf-8'),formato[ext])
			else:
				raise Exception('error de formato en la primer imagen')
		else:
			continue

		repetidos = -1

		for urls in urlsDocuments:
			if urls.has_key('items'):
				for items in urls['items']:
					ext = items['mime']
					if not formato.has_key(ext):
						continue
					link = items['link']

					if not addNodo(raiz,Nodo(link.encode('utf-8'),formato[ext])):
						repetidos += 1

		array = []
		inorden(raiz,array)
		#print array

		header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
		   'Accept': 'text/html, application/xhtml+xml, application/xml',
		   'Accept-Charset': 'ISO-8859-1, utf-8',
		   'Accept-Encoding': 'none',
		   'Connection': 'keep-alive'}

		descargas = 0
		fallos = 0

		for i in array:
			try:
				request = urllib2.Request(i[0], headers=header)
				response = urllib2.urlopen(request, timeout = 3)

				archivo = open(absoluta + '/' + categoria + '/' 
					+ datetime.now().strftime('%d-%m-%Y_%H:%M:%S.%f') 
					+ '.' + i[1],'wb')
				archivo.write(response.read())

				descargas += 1
			except urllib2.URLError as urle:
				print urle, i
				fallos += 1
			except socket.error as se:
				print se, i
				fallos += 1
			except socket.timeout as st:
				print st, i
				fallos += 1
			finally:
				archivo.close()
				response.close()
			print descargas, i

		total = getCountDocumentsByCategoria(categoria)

		print 'links encontrados: ' + str(len(array))
		print 'descargados: ' + str(descargas)
		print 'urls repetidas: ' + str(repetidos)

if __name__ == '__main__':
	main()