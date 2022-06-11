from requests import get
import json
from library_chain.neural_model_serializer import NeuralModelSerializer
from keras.models import model_from_json

class BlockRequestsSender: 
    
    chain = None 

    #CONJUNTO DE FUNCIONES QUE USAREMOS PARA SACAR UN MODELO COMPLETO
    @staticmethod
    def get_serialized_model(block_rest, hash):
        if "http" not in block_rest: 
            block_rest = "http://" + block_rest
        print("LO QUE NOS ESTAMOS TRAYENDO ES ")
        print(get( block_rest +"/get_block", params={'block_hash': hash }).json()) 
        mdl = get( block_rest +"/get_block", params={'block_hash': hash }).json()["block"]['neural_data_transaction'][0]
        print("EL MODEL QUE ESTMAOS TRAYENDO DE VUELTA ES ")
        print(mdl)
        return NeuralModelSerializer.serialize( {"model": mdl["model_arch"], "model_weights": mdl["model_weights"]})
      

    #Function that sends a requests to one server in a block
    @staticmethod
    def get_weights(block_rest,  hash ): 
        return BlockRequestsSender.get_serialized_model( block_rest, hash).get_weights()
        
    #Function that sends a requests to one server in a block
    @staticmethod
    def get_model_arch( block_rest,  hash ): 
        return BlockRequestsSender.get_serialized_model( block_rest, hash).to_json() 

    #Funciones para la firma de los bloques y conseguir datos de los validadores
    @staticmethod
    def get_leader( rest ):
        return str( get(rest ).json()['leader']) #Sacamos el leader desde la chain de los usuario, que será al nodo que llamaremos para firmar el bloque 

    @staticmethod
    def get_dataset(rest ): 
        return get(rest).json()['dataset']

    #Funcion para sacar los validadores de un nodo al que estamos conectados 
    @staticmethod 
    def get_validators(  rest): 
        return get( rest + "/validators"  ).json( ) ['validators'] 
    
    #Verificamos el resultado
    @staticmethod
    def verify_signature( rest, hash, pk ):
        return str( get( rest, params={'hash':hash , 'pk': pk}.json())['result'])

    #FUNCIONA
    @staticmethod
    def sign_leader(rest, hash):
        return str( get( rest , params={'block_hash': hash }).json()['signature'])
        