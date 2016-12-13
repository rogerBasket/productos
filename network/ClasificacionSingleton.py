from Clasificacion import Clasificacion
from constantes import *

print 'singleton clasificacion'

__clazz = Clasificacion(TEST_PATH,IMAGE_WIDTH,IMAGE_HEIGHT,DEPLOY_FILE,MODEL_FILE,MEAN_FILE)
__clazz.start()

__net = __clazz.getNet()
__out = __clazz.getOut()
__transformer = __clazz.getTransformer()

def utilitiesClassification():
	return __net, __out, __transformer

def getImagen():
	return __clazz.imagen