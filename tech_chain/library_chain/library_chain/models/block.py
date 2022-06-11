from hashlib import sha256
from library_chain.models import HashManager
from library_chain.neural_model_serializer import NeuralModelSerializer
import json 
import base64 

class Block: 

    def __init__(self, index, transactions, timestamp, previous_hash, validator  ):
        self.index = index
        self.neural_data_transaction= transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        #self.mkrlroot = MerkleRoot(neural_data_transaction)
        self.nonce = 0.0 #El nonce en los de usuarios lo usaremos como la firma del validador del bloque (Firma el hash del bloque)
        self.model = None
        self.validator = validator #Address (POS)
        self.signature = None #Firma del validador
        self.hash = None
        return 
    
    #HASH BLOCK FILLED WITH 
    #
    # Merkle root + nonce + previous_hash
    def get_hash(self):
        end_hash = HashManager.get_entire_block_hash(self)
        return end_hash

    def model_to_string(self): 
        try:
            return [ self.model.to_json(), self.model.get_weights() ] 
        except Exception as e: 
            print(e)
            return None

    #Function that gets all data transaction
    def get_data(self ): 
        return self.neural_data_transaction

    def get_parsed_model_weight(self , model_weights):
        json_data= {}
        for i in range(0 , len( model_weights)): 
            json_data["n" + str(i)] =   base64.encodebytes(  model_weights[i].tobytes()  ).decode("utf-8")
            json_data["shape n" + str(i)] =  base64.encodebytes(bytes( json.dumps( str( model_weights[i].shape))  , "utf-8" ) ).decode("utf-8")
            
        return json_data

    #Function to get the entire block in a readable format
    def to_string(self ):
        try: 
            return {
                "index": self.index,
                "timestamp": self.timestamp, 
                "previous_hash": self.previous_hash, 
                "hash": self.hash, 
                "model": {
                    "model_arch": self.model.to_json(),
                    "model_weights": self.get_parsed_model_weight( self.model.get_weights())
                }, 
                "validator": self.validator,
                "signature": self.signature, #Firma del modelo 
                "nonce": self.nonce, 
                "neural_data_transaction": self.neural_data_transaction
            }
        except Exception as e: 
            print("HEMOS LANZADO UNA EXCEPCION")
            print(e)
            return {
                "index": self.index,
                "timestamp": self.timestamp, 
                "previous_hash": self.previous_hash, 
                "hash": self.hash, 
                "model": None, 
                "validator": self.validator,
                "signature": self.signature, #Firma del modelo 
                "nonce": self.nonce, 
                "neural_data_transaction": self.neural_data_transaction
            }


    

    
    
    