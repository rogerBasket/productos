from MongoSingleton import getGroups

groups = getGroups()
#print 'groups mongo'

def getAllCategoria():
	return groups.find({},{'_id':0})

def getClaseByNombre(nombre):
	try:
		return groups.find({'nombre':nombre},{'_id':0})
	except StopIteration:
		return None

def getClassAndName():
	try:
		return groups.find({},{'_id':0})
	except:
		return None