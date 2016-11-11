from MongoSingleton import getGroups

groups = getGroups()
#print 'groups mongo'

def getAllCategoria():
	return groups.find({},{'_id':0}).next()['categoria']

def getClaseByNombre(nombre):
	try:
		return groups.find({'categoria.nombre':nombre}).next()['categoria']
	except StopIteration:
		return None

def getClassAndName():
	try:
		return groups.find({},{'_id':0}).next()['categoria']
	except:
		return None