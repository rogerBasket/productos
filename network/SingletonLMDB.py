import lmdb
from constantes import RUTA

TRAIN_LMDB = RUTA+'/train_lmdb'
VALIDATION_LMDB = RUTA+'/validation_lmdb'

__db_train = lmdb.Environment(TRAIN_LMDB, map_size=int(1e12))
__db_validation = lmdb.Environment(VALIDATION_LMDB, map_size=int(1e12))

print 'singleton'

def getTrainDB():
	return __db_train

def getValidationDB():
	return __db_validation

def closeTrain():
	__db_train.close()

def closeValidation():
	__db_validation.close()