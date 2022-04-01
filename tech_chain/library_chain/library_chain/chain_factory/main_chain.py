from library_chain.proof_factory import ProofFactory
from library_chain.models import Block 
from requests import get
from library_chain.api import FederatedLearning


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

    #Function that sends a requests to one server in a block
    def get_weights(self , block_rest,  hash ): 
        return str( get( self.block_rest, params={'hash': hash }).json()['weights']) ç
    
    #Function that sends a requests to one server in a block
    def get_model_arch(self , block_rest,  hash ): 
        return str( get( self.block_rest, params={'hash': hash }).json()['model_arch']) 


    def get_model_from_block(self, block):
        client_wghts = []
        model_arch = None 
        for i in range( 0 , len( block.neural_data_transaction)): 
            if model_arch == None: 
                model_arch = self.get_model_arch(block.neural_data_transaction["rest"] , block.neural_data_transaction["hash"] )
            #La comp está mal, hay que echarle un vistazo 
            
            if model_arch != self.get_model_arch(block.neural_data_transaction["rest"] , block.neural_data_transaction["hash"] )
                return False, "Invalid Blockchain"
            #Tenemos que irnos a cada enlace rest y pillar el bloque con el hash concreto
            client_wgths.append(self.get_weights(block.neural_data_transaction["rest"] , block.neural_data_transaction["hash"] ))
        
        FederatedLearning.
            
    
    @classmethod
    def check_chain_validity(self ):
        
         

    #Function to get a block by hash
    def get_block_by_hash(self, hash): 
        for i in range( 0 , len(chain )): 
            if self.chain[i].hash == hash: 
                return self.chain[i]
        return None 

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