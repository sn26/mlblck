
class HashManager: 

    #Sacamos los hahshes de cada uno de los datos del bloque 
    @staticmethod
    def root_node_hashes(transactions): 
        for i in range(0, len(transactions)): 
            root_hashes = HashManager.get_hash(transactions[i])
        return root_hashes
    
    @staticmethod
    def get_in_pairs( hashes): 
        if (len(hashes ) == 1 or len(hashes ) ==  0 ): 
            return hashes
        if ( len(hashes) == 2):
            return HashManager.get_hash(hashes)
        result = []   
        for i in range(0, len(hashes) - 1): 
            result.append( HashManager.get_in_pairs(hashes[i, i+1 ]))
        return HashManager.get_in_pairs(result)

    @staticmethod
    def gen_hash_tree(transactions ): 
        return HashManager.get_in_pairs(HashManager.root_node_hashes(transactions))
    
    @staticmethod
    def get_hash(transaction):
        return sha256(json.dumps(data.__dict__, sort_keys= True).encode()).hexdigest()

    @staticmethod
    #Function that calculate the hash from one transaction in a whole block
    def get_entire_block_hash( block ): 
        data = list(block.timestamp, block.index, block.nonce, block.previous_hash, HashManager.gen_hash_tree(block.neural_data_transaction) , block.weights)
        return HashManager.get_hash(data)
