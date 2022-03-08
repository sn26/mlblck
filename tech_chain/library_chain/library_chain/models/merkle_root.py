
class MerkleRoot: 

    def __init__(self, transactions):
        self.transactions = transactions 
        return

    #Sacamos los hahshes de cada uno de los datos del bloque 
    def root_node_hashes(self ): 
        for i in range(0, len(self.transactions)): 
            root_hashes = self.get_hash(self.transactions[i])
        return root_hashes
    
    def get_in_pairs(self,  hashes): 
        if (len(hashes ) == 1 or len(hashes ) ==  0 ): 
            return hashes
        if ( len(hashes) == 2):
            return self.get_hash(hashes)
        result = []   
        for i in range(0, len(hashes) - 1): 
            result.append( self.get_in_pairs(hashes[i, i+1 ]))
        return self.get_in_pairs(result)

    def gen_hash_tree(self ): 
        return self.get_in_pairs(self.root_node_hashes())

    #Function that calculate the hash from one transaction in a whole block
    def get_hash(self, data ): 
        return sha256(json.dumps(data.__dict__, sort_keys= True).encode()).hexdigest()
