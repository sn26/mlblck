import tensorflow_federated as tff
import tensorflow as tf
from requests import get
from library_chain.neural_model_serializer import NeuralModelSerializer
from library_chain.api import BlockRequestsSender
import base64 
import gzip 
import json 
import ast

class FederatedLearning: 

    def decode_federated_transaction(transaction):
        print("ESTAMOS PASANDO A REALIZAR LA DECODIFICACION ")
        print("LA TRANSACCION QUE TENEMOS DE ENTRADA ES ")
        print(transaction)
        args = base64.decodebytes( transaction.replace("\"", "").replace("\\n" , "\n").encode("utf-8")) 
        print(args)
        print("AHORA PASAMOS A DESCOMPRIMIRLO")
        args = gzip.decompress( args ).decode("utf-8") 
        print(args)
        print("AHORA ESTAMOS PASANDO A SACAR LO QUE CONTIENE EL ULT BASE  64")
        args = base64.decodebytes( bytes ( args.replace("\"", "").replace("\\n" , "\n").replace("'" , "\"")  , "utf-8")  ).decode("utf-8")
        #Una vez que tenemos los args, nos generaremos el json y luego haremos una lista con los numpy arrays concatenados
        print("EL RESULTADO QUE TENIAMOS ANTES DE PASAR ES ")
        print(args.replace("\\\\", "\\").replace("," , ",\n").replace("'" , "\"").replace("\"{", "{").replace("}\"", "}"))
        res = json.loads(args.replace("\\\\", "\\").replace("," , ",\n").replace("'" , "\"").replace("\"{", "{").replace("}\"", "}")) 
        nodes_lst = []
        counter = 0
        keys_lst=  list( res.keys() ) 
        for i in range(0 ,len(res.keys())): 
            if counter >= len(res.keys()): 
                return nodes_lst, len( keys_lst)/2 
            nodes_lst.append( {
                "rest": ast.literal_eval( base64.decodebytes( bytes( res[keys_lst[counter]] , "utf-8") ).decode("utf-8")), 
                "hash": ast.literal_eval( base64.decodebytes( bytes( res[keys_lst[counter + 1] ] , "utf-8") ).decode("utf-8"))
            })
            counter = counter + 2 
        return nodes_lst, len(keys_lst)/2  

    @staticmethod
    def federated_neural_model_serializer( block, dataset): 
        client_wghts = []
        model_arch = None 
        model = None
        node_lst, clients_total = FederatedLearning.decode_federated_transaction(block.neural_data_transaction[0]['rest_federated_blocks'])
        for i in range( 0 , len( node_lst)): 
            if model == None: 
                model = BlockRequestsSender.get_serialized_model(node_lst[i]["rest"],  node_lst[i]["hash"])
            new_model = BlockRequestsSender.get_serialized_model(node_lst[i]["rest"],  node_lst[i]["hash"])
            #La comparacion del modelo no es correcta, hay que echarle un vistazo
            if model.to_json() != new_model.to_json(): 
                return False, "ERROR: Block not well formed"
            #Concatemos los pesos del modelo que estamos añadiendo
            print("EL MODELO QUE ESTAMOS COMPROBANDO AHORA ES")
            print(new_model.to_json())
            print(new_model.get_weights())
            client_wghts.append(new_model.get_weights())
            print(len(client_wghts))
        print("LA LEN QUE TENEMOS DE CLIENT WEIGHTS ES")
        print(len(client_wghts))
        mean_wght = []
        #SACAMOS LA MEDIA DE TODOS LOS PESOS, PARA CONSEGUIR EL PESO MEDIO DE TODO LO QUE NOS HA ENTRADO
        for i in range( 0, len( client_wghts[0])): 
            sum = client_wghts[0][i] #Cogemos el primero para la suma
            for j in range( 1, len( client_wghts)):
                print( client_wghts[j][i]) 
                sum = sum + client_wghts[j][i]
            sum = sum/len(client_wghts)
            mean_wght.append(sum)
        model.set_weights(mean_wght) #Seteamos los pesos que hemos sacado
        return model
        #Tenemos que devolver un modelo federativo
        '''
        return tff.learning.from_keras_model(
            model,
            input_spec=dataset.element_spec,
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]), client_wghts, clients_total
        '''

    '''
    @tff.tf_computation
    def get_model_from_block( model , client_wghts):
        FederatedLearning.model = model
       
        #Una vez tenemos todos los pesos de los clientes, lo que haremos será llamar al aprendizaje federado 
        #Una vez que hemos actualizado los pesos del servidor, se devolverán para validar el bloque (POL)
        return FederatedLearning.update_server_model(FederatedLearning.get_mean_client_weights(client_wghts))
            
    
    #Function to update all clients with the newest weights version at the main chain
    @tff.tf_computation
    def update_leaf_weights( main_chain ): 
        last_block_weights = main_chain.last_block.model.get_weights()
        #Nos tendremos que ir al último bloque añadido para actualizar los subbloques de los nodos hoja
        for i in range(0 , len(last_block_transactions)):
            BlockRequestsSender.add_weights_transaction(last_block_transactions[i]["rest"] + "/add_transaction")
    ''' 

    #Function to get the median weights from clients
    #@tff.federated_computation
    def get_mean_client_weights(  client_weights, total_clients):
        #Los weights de los clientes los cogeremos de las API Rest (EN realidad aquí metemos también los pesos del servidor)
        return  client_weights/total_clients
        #return tff.federated_mean(client_weights)
 
    '''
    #Funcion que usamos para actualizar los pesos del servidor
    #@tf.function
    @tff.tf_computation
    def server_update_fn( mean_client_weights ):
        # Assign the mean client weights to the server model.
        tf.nest.map_structure(lambda x, y: x.assign(y),
                                FederatedLearning.model.get_weights(), mean_client_weights)
        return FederatedLearning.model_weights

    #Function that recieves a list of weigths and returns the main chain weights (Proofs a main block)
    @tff.tf_computation
    def update_server_model( client_weights): 
        FederatedLearning.model.set_weights( tff.federated_map(FederatedLearning.server_update_fn, FederatedLearning.get_mean_client_weights(client_weights)))
        return FederatedLearning.model
    '''

    @tf.function
    def server_update(model, mean_client_weights):
        """Updates the server model weights as the average of the client model weights."""
        model_weights = model.trainable_variables
        # Assign the mean client weights to the server model.
        tf.nest.map_structure(lambda x, y: x.assign(y),
                                model_weights, mean_client_weights)
        return model_weights


