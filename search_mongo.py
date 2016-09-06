def getDocumentByCategoria(search, categoria):
	return search.find({'categoria':categoria},{'descripcion':1,'categoria':1,'_id':0})