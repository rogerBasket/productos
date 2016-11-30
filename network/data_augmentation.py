#coding=utf-8

from keras.preprocessing.image import ImageDataGenerator

from PIL import Image
import numpy as np

from constantes import *
import os
import glob

datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

def main():
    if not os.path.exists(RUTA + '/procesamiento'):
        exit(0)

    if not os.path.exists(RUTA + '/augmentation'):
        os.makedirs(RUTA + '/augmentation')

    carpetas = glob.glob(RUTA + '/procesamiento/*')

    for carpeta in carpetas:
        carpeta = os.path.abspath(carpeta)
        prefijo = os.path.basename(carpeta)

        if not os.path.isdir(os.path.abspath(carpeta)):
            continue

        if not os.path.exists(RUTA + '/augmentation/' + prefijo):
            os.makedirs(RUTA + '/augmentation/' + prefijo)

        imagenes = glob.glob(carpeta + '/*')

        for imagen in imagenes:
            imagen = os.path.abspath(imagen)


            if prefijo in ['cafe','cigarros','galletas',
                                            'pañales','catsup','talco','sal']:
                continue

            print prefijo, imagen

            if os.path.isdir(imagen):
                continue

            try: 
                img = Image.open(imagen)
                x1 = np.array(list(img.getdata()), dtype = np.float).reshape((img.height, img.width, 3))
                x2 = x1.reshape((1,) + x1.shape)

                for i,batch in enumerate(datagen.flow(x2, batch_size=1,
                                          save_to_dir=RUTA + '/augmentation/' + prefijo,
                                          save_prefix=prefijo, 
                                          save_format='jpeg')):
                    if i == DATA_AUGMENTATION-1:
                        break  # otherwise the generator would loop indefinitely
            except ValueError as ae:
                print imagen
                print ae

if __name__ == '__main__':
    main()

