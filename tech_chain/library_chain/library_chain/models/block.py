from hashlib import sha256
from library_chain.models import HashManager
from library_chain.tools import NeuralModelSerializer

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
        return HashManager.get_entire_block_hash(self)

    #Function that gets all data transaction
    def get_data(self ): 
        return self.transactions 

    #Function to get the entire block in a readable format
    def to_string(self ): 
        return {
            "Timestamp": self.timestamp, 
            "Last Hash": self.previous_hash, 
            "Hash": self.hash, 
            "Model": self.model, 
            "Validator": self.validator,
            "Signature": self.signature, #Firma del modelo 
            "Nonce": self.nonce, 
            "Neural Data Transaction": self.transactions
        }


    

    
    
    