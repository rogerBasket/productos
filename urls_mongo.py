def getTotalResults(search):
	return search.find({},{'_id':0,'kind':0,'url':0,'items':0,'context':0,'queries':0,
		'searchInformation.formattedTotalResults':0,'searchInformation.formattedSearchTime':0,
		'searchInformation.searchTime':0})

def addDescripcion(search, descripcion):
	pass