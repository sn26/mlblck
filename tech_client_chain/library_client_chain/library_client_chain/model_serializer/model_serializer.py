from keras.models import model_from_json
import json 

class ModelSerializer: 

    #Method to get a weights frmo a model
    @staticmethod 
    def serialize( model_json , weights_path ): 
        model = model_from_json(json.dumps(model_json) )
        model.load_weights(weights_path) #Leemos los pesos
        return model
