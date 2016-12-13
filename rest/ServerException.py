class ServerException(Exception):

	def __init__(self, msj):
		self.msj = msj

	def __str__(self):
		return self.msj