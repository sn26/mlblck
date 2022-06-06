from requests import get
import json

class BlockRequestsSender: 
    
    chain = None 

    #Function that sends a requests to one server in a block
    @staticmethod
    def get_weights(block_rest,  hash ): 
        return str( get( block_rest, params={'hash': hash }).json()['model_weights'])
    
    #Function that sends a requests to one server in a block
    @staticmethod
    def get_model_arch( block_rest,  hash ): 
        return str( get( block_rest, params={'hash': hash }).json()['model_arch']) 

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
        