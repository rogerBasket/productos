from pymongo import MongoClient

client = MongoClient()
db = client.google_images

def getUrls():
	return db.urls

def getSearch():
	return db.search

def getGroups():
	return db.groups
