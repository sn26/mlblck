from skimage import exposure
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from PIL import Image
import base64
import numpy as np 
from numpy import asarray

class ImgTooler: 

    img_rows = 32 
    img_cols = 32 

    '''
    def __init__(self):
        self.img_rows, self.img_cols = 32, 32 
        return 
    
    #Esto aqui no tiene sentido, dado que lo haremos en el preprocesado de la chain
    
    def adjust_image( self, gamma, X ):
        for x_i in range(len(X)):
        
            if X[x_i].shape[1] == 3:
                pMin,pMax = np.percentile(X[x_i],(2, 98),axis=0)
            else:
                pMin,pMax = np.percentile(X[x_i],(2, 98),axis=(0,1))
            r_channel = exposure.rescale_intensity(X[x_i][:,:,0], in_range=(pMin[0],pMax[0])) 
            g_channel = exposure.rescale_intensity(X[x_i][:,:,1], in_range=(pMin[1],pMax[1])) 
            b_channel = exposure.rescale_intensity(X[x_i][:,:,2], in_range=(pMin[2],pMax[2])) 
            print("REALOZAMOS LA OPTIMIZACION")
            X[x_i] = np.stack((r_channel,g_channel,b_channel),axis=2)
            X[x_i] = exposure.adjust_log(X[x_i],0.8) 
            X[x_i] = exposure.adjust_sigmoid(X[x_i],0.1) 
            X[x_i]= exposure.adjust_gamma(X[x_i],gamma)
            print("PASAMOS EL AJUSTE")
        return X
    ''' 

    #Necesitamos sacar la imagen 
    #Function to set the data from an image sent by the client and adjust it to the cnn model format (Returns a numpy array )
    @staticmethod 
    def load_image_data(img ):
        #img = Image.open(img_path)
        #Function that encodes a char string into base64 byte string.
        linea_bytes = img.encode('ascii')
        cad = base64.encodebytes(linea_bytes)
        cad_def = cad
        while len(cad_def) < 3072:
            cad_def = cad_def + cad
        img = Image.frombytes("RGB", (ImgTooler.img_rows,ImgTooler.img_cols), cad_def)
        img = img.resize((ImgTooler.img_rows, ImgTooler.img_cols)) #Resizing the image
        return img  #Devolvemos la imagen que compondra nuestro dataset
        '''
        #print(img.size)
        try:
            X = np.ndarray(shape=(1 , self.img_cols, self.img_rows,  3 ),
                     dtype=np.float32)
            X[0] = asarray(img)/255.0
            X = self.adjust_image( 25, X )
            print("SALIMOS DEL AJUSTE")
        except Exception as e: 
            print("ERROR")
            print(e)
        return X[0]
        '''
