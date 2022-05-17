from library_chain.api import BlockRequestsSender

#Class that contains common chains funcionalities between chains
class Common: 
    
    #Para cada nueva transaccion, se comprobaran los campos y la firma
    #Tambien se comprobará la firma de la transaccion
    @staticmethod
    def check_new_transaction( keys, transaction ): 
        for i in range(0, len(transaction.keys())): 
            if transactions.keys()[i] not in keys: 
                return False
        return True

    #Comprobamos la firma en base al hash, la pk del que ha firmado y contra el endpoint de la chain de los usuarios
    @staticmethod
    def verifySignature( self, user_chain , hash , pk ):
        return BlockRequestsSender.verify_signature( user_chain , hash , pk) 
    
    @staticmethod 
    def add_new_transaction( chain , transaction): 
        if chain.check_new_transaction(): 
            if common.verify_signature(chain.user_chain, transaction["digest"] , transaction["from"]) == True: 
                chain.unconfirmed_transactions.append(transaction)
                return True 
        return False

    @staticmethod
    def get_dataset( chain ): 
        return BlockRequestsSender.get_dataset(chain.user_chain + '/dataset')

    @staticmethod 
    def get_response_from_last_block( chain , X): 
        return str( chain.last_block().model.predict(X).argmax(axis=1)[0] )

    @staticmethod
    def get_response_from_hash_block( chain, hash, X): 
        for i in range(0 , len( chain.chain)): 
            if chain.chain[i].hash == hash: 
                return str( chain.chain[i].model.predict(X).argmax(axis=1)[0] )
        return None
    
    #Function to get a block by hash
    @staticmethod
    def get_block_by_hash(chain , hash ): 
        for i in range( 0 , len(chain.chain )): 
            if chain.chain[i].hash == hash: 
                return chain.chain[i]
        return None 

    @staticmethod
    def get_leader( chain ): 
        return BlockRequestsSender.getLeader( chain.user_chain + "/Leader")

    #Añadir un bloque desde los nodos
    @staticmethod
    def mine(chain):
        if len(chain.unconfirmed_transactions) == 0 : 
            return False
        last_block = chain.last_block()
        new_block = Block(index=last_block.index + 1,
                        transactions=chain.unconfirmed_transactions
                        timestamp=time.time(),
                        previous_hash=last_block.hash, 
                        validator= chain.getLeader())
        return chain.add_block(new_block)  

    @staticmethod
    def create_genesis_block(chain ):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0", "0")
        genesis_block.hash = genesis_block.get_hash()
        chain.chain.append(genesis_block)
        return