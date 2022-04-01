import tensorflow_federated as tff

class FederatedLearning: 

    def __init__(self, model ): 
        self.model = model
        return 

    #Function to get the median weights from clients
    def get_mean_client_weights(self , client_weights):
        #Los weights de los clientes los cogeremos de las API Rest (EN realidad aquí metemos también los pesos del servidor)
        return tff.federated_mean(client_weights)
 

    @tf.function
    def server_update_fn( mean_client_weights ):
        # Assign the mean client weights to the server model.
        tf.nest.map_structure(lambda x, y: x.assign(y),
                                self.model.get_weights, mean_client_weights)
        return self.model_weights

    #Function that recieves a list of weigths and returns the main chain weights (Proofs a main block)
    def update_server_model(self, client_weights): 
        return tff.federated_map(server_update_fn, self.get_mean_client_weights(client_weights))



