from requests import get


class BlockRequestsSender: 
    
    #Function that sends a requests to one server in a block
    @staticmethod
    def get_weights(block_rest,  hash ): 
        return str( get( block_rest, params={'hash': hash }).json()['weights'])
    
    #Function that sends a requests to one server in a block
    @staticmethod
    def get_model_arch( block_rest,  hash ): 
        return str( get( block_rest, params={'hash': hash }).json()['model_arch']) 

    #Funciones para la firma de los bloques y conseguir datos de los validadores
    @staticmethod
    def get_leader( rest ):
        return str( get(rest ).json()['leader']) #Sacamos el leader desde la chain de los usuario, que será al nodo que llamaremos para firmar el bloque 

    def get_dataset(rest ): 
        return str(get(rest).json()['dataset'])

    #Verificamos el resultado
    def verify_signature( rest, hash, pk ):
        return str( get( rest, params{'hash':hash , 'pk': pk}.json())['result'])

    def sign_leader(rest, hash):
        return str( get( rest , params={'hash': hash }).json()['signature']) #Llammos para que nos firme el bloque al nodo validador