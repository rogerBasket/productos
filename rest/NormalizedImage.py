import os

from PIL import Image

from .constantes_network import *
from .constantes_service import TEMP

class NormalizedImage:

	def __init__(self, filename):
		self.filename = os.path.abspath(PATH_SERVER + STATIC_PATH_SERVER + TEMP + filename)

	def process(self):
		print 'NormalizedImage - process'

		im = Image.open(self.filename)
		self.fp = im.fp

		return im

	def close(self):
		print 'NormalizedImage - close'

		if not self.fp.closed:
			self.fp.close()
