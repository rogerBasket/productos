from MongoSingleton import getSearch

search = getSearch()
#print 'search mongo'

def getDocumentByCategoria(categoria):
	return search.find({'categoria':categoria},{'descripcion':1,'categoria':1,'_id':0}).next()

def getTotalResultsByCategoria(categoria):
	return search.find({'categoria':categoria},{'_id':0,'categoria':0,
		'descripcion.nombre':0}).next()['descripcion']