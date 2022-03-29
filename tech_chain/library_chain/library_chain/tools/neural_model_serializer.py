from keras.models import model_from_json

class NeuralModelSerializer: 

    def __init__(self ):
        return

    #Method to get a weights frmo a model
    @staticmethod 
    def serialize(self, block): 
        model = model_from_json(block["model"] )
        model.set_weights(block["weights"])
        return model
