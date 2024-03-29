import collections
from sklearn import metrics
import keras
import numpy

class ProofOfLearning: 

    def __init__(self):
        return 

    #Function to know if a model is better than the actual block
    def proof(self, model_chain, model_block, dataset ):
        if( self.precission_acc(model_chain.predict(dataset["x_test"]), dataset["y_test"]) >=  self.precission_acc(model_block.predict(dataset["x_test"]), dataset["y_test"])): 
            return False
        #Si con el modelo se mejora la precisión, entonces será válido para ser añadido 
        return True

    #Function to get the nonce of a block
    def nonce(self, block, dataset): 
        return self.precission_acc(block.model.predict(dataset["x_test"]), dataset["y_test"])

    #Function to get the precission rate of a model trained
    def precission_acc(self, y_pred , y_test):
        y_pred = keras.utils.to_categorical(y_pred, 4)
        y_test = keras.utils.to_categorical(y_test, 4)
        print("EL PRED INICIAL ES ")
        print(y_pred)
        '''
        prec_hang= 0.00
        ape_media_hang = 0.00
        for i in range(len(y_pred)):
            #Getting the precission acc of each entry 
            #SDC AND HANG? 
            ape_hang = abs(y_test[i][0] - y_pred[i][0] ) / y_test[i][0] 
            if ape_hang < 0.05: 
                ape_media_hang = ape_media_hang + 1
            if y_test[i][0] ==0.00 and y_pred[i][0] == 0.00:
                p_hang = 1.0
                #p_hang = 1 - abs(abs(y_pred[i][0]) - abs(y_test[i][0]))/abs(abs(y_test[i][0])+abs(y_pred[i][0]))
                #if p_hang < 0.95: p_hang = 0.0
            else:
                p_hang = 1 - (abs(abs(y_pred[i][0]) - abs(y_test[i][0]))/abs(abs(y_test[i][0])+abs(y_pred[i][0])))
            prec_hang =  prec_hang + p_hang 
        prec_hang = prec_hang / len(y_pred)
        ape_media_hang = ape_media_hang /  len(y_pred)
        print("PACC_5 MEDIA HANG : " , ape_media_hang)
        ''' 
        print(numpy.argmax(y_test, axis=1))
        print(numpy.argmax(numpy.argmax(y_pred, axis=1), axis=1))
        return metrics.accuracy_score(numpy.argmax(y_test, axis=1) ,numpy.argmax(numpy.argmax(y_pred, axis=1), axis=1))
        
        

