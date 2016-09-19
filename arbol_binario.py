import numpy as np
from Nodo import Nodo
from ABB import *

def main():
	aleatorios = []

	for i in np.arange(10):
		aleatorios.append(np.random.randint(20))

	raiz = Nodo(aleatorios[0])
	print raiz.getUrl()

	for i in np.arange(1,10):
		addNodo(raiz,Nodo(aleatorios[i]))

	print 'aleatorios: ', aleatorios

	array = []
	print 'inorden: ',
	inorden(raiz,array)
	print array

	array = []
	print 'preorden: ',
	preorden(raiz,array)
	print array

	array = []
	print 'postorden: ',
	postorden(raiz,array)
	print array

if __name__ == '__main__':
	main()