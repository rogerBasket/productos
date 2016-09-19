from MongoSingleton import getGroups

groups = getGroups()
#print 'groups mongo'

def getAllCategoria():
	return groups.find({},{'_id':0}).next()['categoria']
