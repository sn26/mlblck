from library_chain.proof_factory import ProofFactory
from library_chain.models import Block, HashManager 
from libary_chain.tools import DataLoader

#EN LOS NODOS HOJA, CADA BLOQUE LLEVA: TRANSACTION { PESOS  + MODEL_ARCH }
#PARA AÑADIR A LOS NODOS HOJA, SE ESTABLECE UN MODELO DE POL SOBRE LA PROPIA CADENA  (EL DATASET VIENE HEREDADO DEL NODO PADRE ( BUSCAR MANERA DE QUE CUANDO SE REGISTRE, SE REGISTRE EL NODO))
#
# MANERA DE COGER EL DATASET DEL PADRE -> ENDPOINT EN LA CHAIN PADRE
#
class RootChain: 

    identifier = 1

    def __init__(self ): 
        #self.size_per_block = size_per_block #En los nodos hoja sólo dejaremos 1 de tam
        self.chain = []
        self.proof_cls = ProofFactory(MainChain.identifier).create_proof()
        self.unconfirmed_transactions = [] #Transacciones que se encuentran por incluir en la cadena
        return
    
    @property 
    def last_block(self ): 
        return self.chain[-1].hash
    
    #Checking if a transaction has the minimum values to being a blog
    def check_new_transaction(self, transaction):
        if ( len(transaction.keys()) == 4 and "timestamp" in transaction.keys() and "author" in transaction.keys() and "weights" in transaction.keys() and "model_arch" in transaction.keys() ):
            return True
        return False
   
    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction): 
        if self.check_new_transaction(transaction): 
            self.unconfirmed_transactions.append(transaction)
            return True
        return False

    def add_block(self, block):
        if len( block.neural_data_transaction) > 1: 
            #Solo permitiremos que se añadan bloques con 1 transaccion
            return False 
        if self.chain[-1].hash != block.previous_hash:
            return False
        result, model  =self.proof(block)
        if result == True: 
            block.nonce = self.proof_cls.nonce(block) #Sacamos la precisión del bloque
            block.hash = block.set_hash() #Calculamos el hash del bloque
            block.model = model
            self.chain.append(block)
            return True
        return False

    #Lo tenemos que cambiar, dado que ahora el proof se realiza solamente sobre el modelo del bloque en el que nos encontramos y sobre el dataset que nos enontramos dentro del chain 
    def proof(self, block ):
        model_block = NeuralModelSerializer.serialize(block.neural_data_transaction[0]["model_arch"])
        if( self.proof_cls.proof(model_chain, model_block )): 
            return True, model_block
        return False, None
    
    #Function to get a response of a prediction fronm a specific block
    def get_response_from_hash_block(self, hash, X  ): 
        for i in range(0 , len( chain)): 
            if chain[i].hash == hash: 
                return str( chain[i].predict(X).argmax(axis=1)[0] )
        return None
    
    #SSacamos la predicción del último bloque
    def get_response_from_last_block(self, X):
        return str( self.last_block().predict(X).argmax(axis=1)[0] )
                
    #Funcion que comprueba: 
    #HASH DEL BLOQUE CALCULANDO EL NONCE 
    #PROOF DE LA PREC EN COMPARACION CON EL BLOQUE ANTERIOR
    @classmethod
    def is_valid_proof(cls, block , block_hash,  last_block ): 
        proof_cls = ProofFactory(MainChain.identifier).create_proof()
        block_model = NeuralModelSerializer.serialize(BlockRequestsSender.get_model_arch( block.neural_data_transaction[0]["rest"], block.neural_data_transaction[0]["hash"]))
        block_model.nonce = proof_cls.nonce(block)
        if last_block != None: 
            last_block_model = NeuralModelSerializer.serialize(BlockRequestsSender.get_model_arch( last_block.neural_data_transaction[0]["rest"], last_block.neural_data_transaction[0]["hash"]))
            if (proof_cls.proof( last_block_model, block_model )): 
                block.hash = HashManager.get_entire_block_hash( block )
                if block.hash == block_hash and last_block.hash == block.previous_hash:
                    return True
            return False
        block.hash = HashManager.get_entire_block_hash( block )
        if block.hash == block_hash:
            return True 
        return False 

    @classmethod
    def check_chain_validity(cls, chain ):
        result = True
        previous_hash = "0"
        last_block = None
        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")
            if not cls.is_valid_proof(block, block_hash, last_block  ) or \
                    last_block.hash != block.previous_hash:
                return False
            last_block = block
        return True

    #Function to get a block by hash
    def get_block_by_hash(self, hash): 
        for i in range( 0 , len(chain )): 
            if self.chain[i].hash == hash: 
                return self.chain[i]
        return None 

    #Añadir un bloque desde los nodos
    def mine(self):
        if len(self.unconfirmed_transactions == 0 ): 
            return False
        last_block = self.last_block()
        new_block = Block(index=last_block.index + 1,
                        transactions=self.unconfirmed_transactions,
                        timestamp=time.time(),
                        previous_hash=last_block.hash)
        return self.add_block(new_block)  

    def create_genesis_block(self ):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.get_hash()
        self.chain.append(genesis_block)
        return

