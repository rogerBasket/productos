def getDocumentByCategoria(search, categoria):
	return search.find({'categoria':categoria},{'categoria':0,'_id':0})