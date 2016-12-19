import numpy as np
import lmdb
import caffe

from objetos import productos
from constantes import *

def main():
	print RUTA

	db = lmdb.open(RUTA + '/train_lmdb', readonly = True)
	tx = db.begin()

	cursor = tx.cursor()
	for key, value in cursor:
		print key

		datum = caffe.proto.caffe_pb2.Datum()
		datum.ParseFromString(value)

		flat_x = np.fromstring(datum.data, dtype=np.uint8)
		x = flat_x.reshape(CANELES, datum.height, datum.width)
		y = datum.label

	db.close()

if __name__ == '__main__':
	main()