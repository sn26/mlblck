from hashlib import sha256
from library_chain.models import HashManager
from library_chain.tools import NeuralModelSerializer

class Block: 

    def __init__(self, index, neural_data_transaction, timestamp, previous_hash ):
        self.index = index
        self.neural_data_transaction = neural_data_transaction 
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        #self.mkrlroot = MerkleRoot(neural_data_transaction)
        self.nonce = 0.0
        self.model = None
        self.hash = None
        return 
    
    #HASH BLOCK FILLED WITH 
    #
    # Merkle root + nonce + previous_hash
    def get_hash(self):
        return HashManager.get_entire_block_hash(self)

    #Function that gets all data transaction
    def get_data(self ): 
        return self.neural_data_transaction 

    

    
    
    