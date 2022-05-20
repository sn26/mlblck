from library_chain.chain_factory import Common
from library_chain.proof_factory import ProofFactory
from library_chain.api import BlockRequestsSender
from library_chain.models import Block, HashManager 

#EN LOS NODOS HOJA, CADA BLOQUE LLEVA: TRANSACTION { PESOS  + MODEL_ARCH }
#PARA AÑADIR A LOS NODOS HOJA, SE ESTABLECE UN MODELO DE POL SOBRE LA PROPIA CADENA  (EL DATASET VIENE HEREDADO DEL NODO PADRE ( BUSCAR MANERA DE QUE CUANDO SE REGISTRE, SE REGISTRE EL NODO))
#
# MANERA DE COGER EL DATASET DEL PADRE -> ENDPOINT EN LA CHAIN PADRE
#
# REALIZA LOS MISMOS PASOS QUE LA PADRE, SOLO QUE AHORA EL PROOF NO TENDRÁ QUE IRSE A LA REQUESTS DE LOS HIJOS PARA SACAR LOS DATOS, SINO QUE LOS SACAREMOS EN BASE A LO QUE TENGAMOS EN NUESTRO NODO
class RootChain: 

    identifier = 1

    def __init__(self ): 
        #self.size_per_block = size_per_block #En los nodos hoja sólo dejaremos 1 de tam
        self.chain = []
        self.proof_cls = ProofFactory.create_proof(RootChain.identifier)
        self.unconfirmed_transactions = [] #Transacciones que se encuentran por incluir en la cadena
        self.user_chain = "" #Enlace rest a nuestra cadena con los usuarios compartidos por todas las chains    
        return
    
    @property 
    def last_block(self ): 
        return self.chain[-1].hash

    @classmethod
    def set_user_chain(cls , user_chain ): 
        cls.user_chain= user_chain 
        return 

    @property 
    def last_block(self ): 
        return self.chain[-1].hash
    
    #Checking if a transaction has the minimum values to being a blog
    def check_new_transaction(self, transaction):
        return Common.check_new_transaction( ["timestamp", "pk", "model_arch", "weights", "digest"], transaction)
    
    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction): 
        return Common.add_new_transaction( cahin, transaction )

    def add_block(self, block):
        if len( block.neural_data_transaction) > 1: 
            #Solo permitiremos que se añadan bloques con 1 transaccion
            return False 
        if self.chain[-1].hash != block.previous_hash:
            return False
        result, model  =self.proof(block)
        if result == True: 
            block.nonce = self.proof_cls.nonce(block, self.get_dataset()) #Sacamos la precisión del bloque en base a los pesos del bloque y en base al dataset del validador que tenemos en la chain de los usuarios
            block.hash = block.get_hash() #Calculamos el hash del bloque
            block.model = model
            block.signature=  BlockRequestsSender.sign_leader(self.user_chain + "/sign" , block.get_hash())
            self.chain.append(block)
            return True
        return False

    def get_dataset(self ): 
        return Common.get_dataset( self)

    #Lo tenemos que cambiar, dado que ahora el proof se realiza solamente sobre el modelo del bloque en el que nos encontramos y sobre el dataset que nos enontramos dentro del chain 
    def proof(self, block ):
        model_block = NeuralModelSerializer.serialize({ "model": block.transactions[0]["model_arch"] , "weights": block.transactions[0]["weights"]})
        if( self.proof_cls.proof(self.last_block.model , model_block, self.get_dataset() )): 
            return True, model_block
        return False, None
    
    #Function to get a response of a prediction fronm a specific block
    def get_response_from_hash_block(self, hash, X  ): 
        return Common.get_response_from_hash_block(self , hash , X )
    
    #SSacamos la predicción del último bloque
    def get_response_from_last_block(self, X):
        return Common.get_response_from_last_block( self , X )
                
    #Funcion que comprueba: 
    #HASH DEL BLOQUE CALCULANDO EL NONCE 
    #PROOF DE LA PREC EN COMPARACION CON EL BLOQUE ANTERIOR
    @classmethod
    def is_valid_proof(cls, block , block_hash,  last_block ): 
        proof_cls = ProofFactory(MainChain.identifier).create_proof()
        block_model = NeuralModelSerializer.serialize(block.neural_data_transaction[0]["model_arch"] , block.neural_data_transaction[0]["weights"] )
        block_model.nonce = proof_cls.nonce(block, self.get_dataset())
        if last_block != None: 
            last_block_model = NeuralModelSerializer.serialize(block.neural_data_transaction[0]["model_arch"] , block.neural_data_transaction[0]["weights"] )
            if (proof_cls.proof( last_block_model, block_model , self.get_dataset())): 
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
        return Common.get_block_by_hash( self , hash)

    def get_leader( self ): 
        return Common.get_leader( self)

    #Añadir un bloque desde los nodos
    def mine(self):
        return Common.mine(self)

    def create_genesis_block(self , wallet ):
        return Common.create_genesis_block(self , wallet )
