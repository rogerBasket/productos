import urllib2
import os
from datetime import datetime
import socket
import httplib

from Nodo import Nodo
from ABB import addNodo, inorden
from urls_mongo import *
from groups_mongo import getAllCategoria
from constantes import RUTA

formato = {
	'image/jpeg':'jpg',
	'image/png':'png'
}

def main():
	if os.path.exists(RUTA):
		absoluta = os.path.abspath(RUTA)
	else:
		return

	categoriasGroups = getAllCategoria()

	for categoria in categoriasGroups:
		categoriaNombre = categoria['nombre']
		
		print categoriaNombre

		if categoriaNombre in ['pantalon','tenis','rastrillo']:
			continue

		if not os.path.exists(absoluta + '/' + categoriaNombre):
			os.makedirs(absoluta + '/' + categoriaNombre)

		print 'nombre de categoria: ' + categoriaNombre

		urlsDocuments = getInfoUrlsByCategoria(categoriaNombre)

		first = getFirstByCategoria(categoriaNombre)
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

		archivo = None
		response = None

		for i in array:
			try:
				request = urllib2.Request(i[0], headers=header)
				response = urllib2.urlopen(request, timeout = 3)

				archivo = open(absoluta + '/' + categoriaNombre + '/' 
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
			except httplib.BadStatusLine as bsl:
				print bsl, i
				fallos += 1
			except httplib.IncompleteRead as ir:
				print ir, i
				fallos += 1
			finally:
				if archivo != None:
					archivo.close()
				if response != None:
					response.close()
			print descargas, i

		total = getCountDocumentsByCategoria(categoriaNombre)

		print 'links encontrados: ' + str(len(array))
		print 'descargados: ' + str(descargas)
		print 'urls repetidas: ' + str(repetidos)

if __name__ == '__main__':
	main()