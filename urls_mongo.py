from MongoSingleton import getUrls

urls = getUrls()
#print 'urls mongo'

def getTotalResults():
	return urls.find({},{'_id':0,'kind':0,'url':0,'items':0,'context':0,'queries':0,
		'searchInformation.formattedTotalResults':0,'searchInformation.formattedSearchTime':0,
		'searchInformation.searchTime':0,'categoria':0,
		'descripcion':0,'spelling':0}).next()['searchInformation']['totalResults']

def getFindCategoria(categoria):
	try:
		return urls.find({'categoria':categoria},{'_id':0,'kind':0,'url':0,'items':0,'context':0,'queries':0,
			'searchInformation':0,'descripcion':0,'spelling':0}).limit(1).next()['categoria']
	except StopIteration:
		return None

def getCountDocumentsByCategoria(categoria):
	return urls.find({'categoria':categoria}).count()

def deleteUrlsByCategoria(categoria):
	respuesta = urls.remove({'categoria':categoria})
	if respuesta['ok'] != 1:
		raise Exception('error al eliminar categoria = ' + categoria)

def addDocumentInUrls(document):
	urls.insert(document)

def getTotalDocumentsUrls():
	return urls.find().count()

def getInfoUrlsByCategoria(categoria):
	return urls.find({'categoria':categoria},{'_id':0,'kind':0,'url':0,'context':0,
		'queries':0,'searchInformation':0,'items.kind':0,'items.title':0,
		'items.displayLink':0,'items.htmlTitle':0,'items.snippet':0,
		'items.htmlSnippet':0,'items.image':0,'items.fileFormat':0})

def getFirstByCategoria(categoria):
	try:
		return urls.find({'categoria':'refresco'},{'_id':0,'kind':0,'url':0,'context':0,
			'queries':0,'searchInformation':0, 'items.kind':0,'items.title':0,
			'items.displayLink':0,'items.htmlTitle':0,'items.snippet':0,
			'items.htmlSnippet':0, 'items.image':0,'items.fileFormat':0,'categoria':0,
			'descripcion':0}).limit(1).next()['items'][0]
	except StopIteration:
		return None