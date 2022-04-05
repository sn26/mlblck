import tensorflow_federated as tff
from requests import get
from library_chain.tools import NeuralModelSerializer
from library_chain.api import BlockRequestsSender

class FederatedLearning: 

    def __init__(self, model): 
        self.model = model 
        return 

    def get_model_from_block(self, block):
        client_wghts = []
        model_arch = None 
        for i in range( 0 , len( block.neural_data_transaction)): 
            if model_arch == None: 
                model_arch = BlockRequestsSender.get_model_arch(block.neural_data_transaction[i]["rest"] , block.neural_data_transaction[i]["hash"] )
            #La comparacion del modelo no es correcta, hay que echarle un vistazo
            if model_arch != BlockRequestsSender.get_model_arch(block.neural_data_transaction[i]["rest"] , block.neural_data_transaction[i]["hash"] )
                return False, "ERROR: Block not well formed"
            #Tenemos que irnos a cada enlace rest y pillar el bloque con el hash concreto
            client_wgths.append(BlockRequestsSender.get_weights(block.neural_data_transaction[i]["rest"] , block.neural_data_transaction[i]["hash"] ))
        #Checking if the model arch of the leaf blocks are the same of the server model 
        model_nblck = NeuralModelSerializer.serialize(block)
        if model_nblck != self.model: 
            self.model = model_nblck

        #Una vez tenemos todos los pesos de los clientes, lo que haremos será llamar al aprendizaje federado 
        #Una vez que hemos actualizado los pesos del servidor, se devolverán para validar el bloque (POL)
        return self.update_server_model(self.get_mean_client_weights(client_wghts))
            


    #Function to update all clients with the newest weights version at the main chain
    def update_leaf_weights(self, main_chain ): 
        last_block_transactions = main_chain.last_block().transactions
        from i in range(0 , len(last_block_transactions)):
            if
            


    #Function to get the median weights from clients
    def get_mean_client_weights(self , client_weights):
        #Los weights de los clientes los cogeremos de las API Rest (EN realidad aquí metemos también los pesos del servidor)
        return tff.federated_mean(client_weights)
 

    #Funcion que usamos para actualizar los pesos del servidor
    @tf.function
    def server_update_fn( mean_client_weights ):
        # Assign the mean client weights to the server model.
        tf.nest.map_structure(lambda x, y: x.assign(y),
                                self.model.get_weights(), mean_client_weights)
        return self.model_weights

    #Function that recieves a list of weigths and returns the main chain weights (Proofs a main block)
    def update_server_model(self, client_weights): 
        self.model.set_weights( tff.federated_map(self.server_update_fn, self.get_mean_client_weights(client_weights)))
        return self.model



