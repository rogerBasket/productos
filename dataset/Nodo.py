class Nodo:

	def __init__(self, url, ext = 'jpg', izq = None, der = None):
		if url != None:
			#if isinstance(url,int):
			if isinstance(url,str):
				self.__url = url
			else:
				raise Exception('url no es instancia de str')
		else:
			raise Exception('url no puede ser None')

		if ext != None:
			if isinstance(ext,str):
				self.__ext = ext
			else:
				raise Exception('ext no es instancia de str')
		else:
			raise Exception('ext no puede ser None')

		if izq != None:
			if isinstance(izq,Nodo):
				self.__izq = izq
			else:
				raise Exception('izq no es instancia de Nodo')
		else:
			self.__izq = izq

		if der != None:
			if isinstance(der,Nodo):
				self.__der = der
			else:
				raise Exception('der no es instancia de Nodo')
		else:
			self.__der = der

	def getUrl(self):
		return self.__url

	def getExt(self):
		return self.__ext

	def setIzq(self, izq):
		self.__izq = izq

	def getIzq(self):
		return self.__izq

	def setDer(self, der):
		self.__der = der

	def getDer(self):
		return self.__der
