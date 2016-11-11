def addNodo(raiz, nodo):
	if raiz.getUrl() > nodo.getUrl():
		if raiz.getIzq() != None:
			return addNodo(raiz.getIzq(),nodo)
		else:
			raiz.setIzq(nodo)
			return True
	elif raiz.getUrl() < nodo.getUrl():
		if raiz.getDer() != None:
			return addNodo(raiz.getDer(),nodo)
		else:
			raiz.setDer(nodo)
			return True
	else:
		return False

def inorden(raiz, array):
	if raiz.getIzq() != None:
		inorden(raiz.getIzq(),array)
	array.append((raiz.getUrl(),raiz.getExt()))
	if raiz.getDer() != None:
		inorden(raiz.getDer(),array)

def preorden(raiz, array):
	array.append((raiz.getUrl(),raiz.getExt()))
	if raiz.getIzq() != None:
		preorden(raiz.getIzq(),array)
	if raiz.getDer() != None:
		preorden(raiz.getDer(),array)

def postorden(raiz, array):
	if raiz.getIzq() != None:
		postorden(raiz.getIzq(),array)
	if raiz.getDer() != None:
		postorden(raiz.getDer(),array)
	array.append((raiz.getUrl(),raiz.getExt()))