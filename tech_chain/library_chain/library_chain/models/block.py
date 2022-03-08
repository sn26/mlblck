from hashlib import sha256
from library_chain.models import MerkleRoot

class Block: 

    def __init__(self, index, neural_data_transaction, timestamp ):
        self.index = index
        self.neural_data_transaction = neural_data_transaction 
        self.timestamp = timestamp
        return 

    
    
    