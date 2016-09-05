from pymongo import MongoClient

from images_mongo import getTotalResults

def main():
	client = MongoClient()
	db = client.google_images
	search = db.search

	totalResults = getTotalResults(search).next()
	print totalResults['searchInformation']['totalResults']

if __name__ == '__main__':
	main()