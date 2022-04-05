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