from library_chain.proof_factory import ProofFactory
from library_chain.models import Block 

class MainChain: 
 
    def __init__(self, id, size_per_block): 
        self.size_per_block = size_per_block #En los nodos hoja sólo dejaremos 1 de tam
        self.chain = []
        self.identifier = id
        self.proof_cls = ProofFactory(self.identifier).create_proof()
        self.unconfirmed_transaction = [] #Transacciones que se encuentran por incluir en la cadena
        return
    
    @property 
    def last_block(self ): 
        return self.chain[-1].hash
    
    #Checking if a transaction has the minimum values to being a blog
    def check_new_transaction(self, transaction):
        if ( len(transaction.keys()) == 2 and "child_hash" in transaction.keys() and "rest" in transaction.keys() ):
            return True
        return False

   
    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction): 
        if self.check_new_transaction(transaction): 
            self.unconfirmed_transaction.append(transaction)
            return True
        return False

    def add_block(self, block):
        if self.chain[-1].hash != block.previous_hash:
            return False
        if self.proof(block): 
            block.nonce = self.proof_cls.nonce(block) #Sacamos la precisión del bloque
            block.hash = block.set_hash() #Calculamos el hash del bloque
            self.chain.append(block)

    def proof(self, block ):
        if( self.proof_cls.proof( self.chain[-1], block )): 
            return True
        return False

    @classmethod
    def check_chain_validity(self ):
         

    
    #Añadir un bloque desde los nodos
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block()
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        self.add_block(new_block)
        self.unconfirmed_transactions.clear()
        return True