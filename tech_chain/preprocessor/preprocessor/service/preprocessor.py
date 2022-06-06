from skimage import exposure
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from PIL import Image
import base64
import numpy as np 
from numpy import asarray
from sklearn.utils import shuffle
import gzip
import json

class Preprocessor: 

    img_rows, img_cols = 32, 32

    labels = {
        'buffer_of': 0, 
        'bwget': 1, 
        'normal': 2,
        'traversal': 3
    }       

    @staticmethod
    def calculate_length(dataset):
        total_length = 0 
        for key in dataset.keys(): 
            total_length = total_length + len(dataset[key])
        return total_length

    #Funcion que nos permite realizar el ajuste de una imagen
    @staticmethod
    def adjust_image(  gamma, x_i ):
        if x_i.shape[1] == 3:
            pMin,pMax = np.percentile(x_i,(2, 98),axis=0)
        else:
            pMin,pMax = np.percentile(x_i,(2, 98),axis=(0,1))
        r_channel = exposure.rescale_intensity(x_i[:,:,0], in_range=(pMin[0],pMax[0])) 
        g_channel = exposure.rescale_intensity(x_i[:,:,1], in_range=(pMin[1],pMax[1])) 
        b_channel = exposure.rescale_intensity(x_i[:,:,2], in_range=(pMin[2],pMax[2])) 
        print("REALOZAMOS LA OPTIMIZACION")
        x_i = np.stack((r_channel,g_channel,b_channel),axis=2)
        x_i = exposure.adjust_log(x_i,0.8) 
        x_i = exposure.adjust_sigmoid(x_i,0.1) 
        x_i= exposure.adjust_gamma(x_i,gamma)
        print("PASAMOS EL AJUSTE")
        return x_i

    #El preprocess dado un dataset de entrada tendra 
    #que sacar la imagen de cada elemento del array y 
    #luego ya hacer un numpy resultado de todo el json de entrada
    @staticmethod
    def preprocess( dataset): 
        total_length = Preprocessor.calculate_length( dataset )
        X = np.ndarray(shape=(total_length , Preprocessor.img_cols, Preprocessor.img_rows,  3 ),
                            dtype=np.float32)
        y = np.ndarray(shape=(total_length   ),
                     dtype=np.int32)
        iterator = 0 
        for key in dataset.keys(): 
            for  i in range(0 ,len( dataset[key])):
                #Decodificamos y descomprimimos para poder usarlo 
                dataset[key][i] = base64.decodebytes( dataset[key][i].replace("\"", "").replace("\\n" , "\n").encode("utf-8"))
                dataset[key][i] = gzip.decompress( dataset[key][i] )
                img = Image.frombytes("RGB", (Preprocessor.img_rows,Preprocessor.img_cols), dataset[key][i])
                img = img.resize((Preprocessor.img_rows, Preprocessor.img_cols)) #Resizing the image
                #print(img.size)
                try: 
                    X[iterator] = asarray(img)/255.0
                    X[iterator]= Preprocessor.adjust_image( 2, X[iterator] )
                    X[iterator]= img
                    y[iterator] = Preprocessor.labels[key]
                    print(y[iterator])
                except Exception as e: 
                    print("ERROR: Something were wrong while preprocessing data")
                    print(e)
                iterator = iterator + 1 
        X, y = shuffle(X, y, random_state=0)
        print("LA Y QUE TENEMOS ES ")
        print(y)
        return { "x_test": X, "y_test": y }




    