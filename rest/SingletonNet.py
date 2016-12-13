from . import util_net

__net, __transformer = util_net.initializedNet()

def getNet():
	return __net

def getTransformer():
	return __transformer
	