from Clasificacion import Clasificacion
import constantes as cnt

print 'singleton clasificacion'

__clazz = Clasificacion(cnt.RUTA,cnt.IMAGE_WIDTH,cnt.IMAGE_HEIGHT,cnt.DEPLOY_FILE,cnt.MODEL_FILE,cnt.MEAN_FILE)
__clazz.start()

__net = __clazz.getNet()
__out = __clazz.getOut()
__transformer = __clazz.getTransformer()

def utilitiesClassification():
	return __net, __out, __transformer

def getImagen():
	return __clazz.imagen