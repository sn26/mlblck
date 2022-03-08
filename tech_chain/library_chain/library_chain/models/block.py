from hashlib import sha256
from library_chain.models import MerkleRoot

class Block: 

    def __init__(self, index, neural_data_transaction, timestamp, previous_hash ):
        self.index = index
        self.neural_data_transaction = neural_data_transaction 
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.mkrlroot = MerkleRoot(neural_data_transaction)
        self.hash = self.set_hash()
        return 

    def set_hash(self):
        return self.get_hash( list( self.previous_hash, self.mkrlroot))
    
    #Function that calculate the hash from one transaction in a whole block
    def get_hash (self, data ): 
        return sha256(json.dumps(data.__dict__, sort_keys= True).encode()).hexdigest()

    

    
    
    