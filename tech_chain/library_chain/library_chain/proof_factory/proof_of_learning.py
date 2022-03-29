
class ProofOfLearning: 

    def __init__(self):
        self.dataset = []
        self.model = None
        return 
    
    #Function to know if a model is better than the actual block
    def proof(self, last_block, block ):
        from library_chain.tools import NeuralModelSerializer
        model_nblck = NeuralModelSerializer.serialize(block)
        if( self.precission_acc(NeuralModelSerializer.serialize(last_block).predict(self.dataset["x_test"]), self.dataset["y_test"]) >=  self.precission_acc(model.predict(self.dataset["x_test"]), self.dataset["y_test"])): 
            return False 
        return True

    #Function to get the nonce of a b
    def nonce(self, block): 
        return self.precission_acc(model.predict(self.dataset["x_test"]), self.dataset["y_test"])

    #Function to get the precission rate of a model trained
    def precission_acc(self, y_pred , y_test):
        prec_sdc= 0.00
        prec_hang= 0.00
        ape_media_sdc = 0.00
        ape_media_hang = 0.00
        for i in range(len(y_pred)):
            #Getting the precission acc of each entry 
            #SDC AND HANG?
            ape_sdc = abs(y_test[i][1] - y_pred[i][1] ) / y_test[i][1] 
            ape_hang = abs(y_test[i][0] - y_pred[i][0] ) / y_test[i][0] 
            if ape_sdc < 0.05: 
            ape_media_sdc +=1
            if ape_hang < 0.05: 
            ape_media_hang +=1
            if y_test[i][1] ==0.00 and y_pred[i][1] == 0.00:
                #print("ENTRANDO")
                p_sdc = 1
                p_hang = 1 - abs(abs(y_pred[i][0]) - abs(y_test[i][0]))/abs(abs(y_test[i][0])+abs(y_pred[i][0]))
                #if p_hang < 0.95: p_hang = 0.0
            else:
                p_hang = 1 - abs(abs(y_pred[i][0]) - abs(y_test[i][0]))/abs(abs(y_test[i][0])+abs(y_pred[i][0]))
                p_sdc = 1 -  abs(abs(y_pred[i][1]) - abs(y_test[i][1]))/abs(y_test[i][1]+y_pred[i][1])
                '''
                if p_hang < 0.95: 
                    p_hang = 0.0
                if p_sdc < 0.95: 
                    p_sdc = 0.0
                '''
            prec_sdc += p_sdc
            prec_hang += p_hang 
    
        prec_sdc = prec_sdc / len(y_pred)
        prec_hang = prec_hang / len(y_pred)
        ape_media_sdc = ape_media_sdc / len(y_pred)
        ape_media_hang = ape_media_hang /  len(y_pred)
        print("PACC_5 MEDIA UNACE : " , ape_media_sdc)
        print("PACC_5 MEDIA HANG : " , ape_media_hang)
        return prec_sdc, prec_hang

    
    #Function that sets the dastaset which is going to use for checking the acc of a block
    def set_dataset(self, dataset, preprocessor  ):
        self.dataset = preprocessor.preprocess(dataset)
        return  
    


        