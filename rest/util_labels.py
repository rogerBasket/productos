from .constantes_network import *

def readLabels():
	file = None

	try:
		file = open(PATH_SERVER + STATIC_PATH_SERVER + NET + LABELS_FILE,'r')
		labels = []

		for linea in file.readlines():
			if linea != '\n':
				labels.append(linea[:-1])

		return labels
	finally:
		if file != None:
			file.close()

	return []