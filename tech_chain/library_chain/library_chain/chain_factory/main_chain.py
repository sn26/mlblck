from library_chain.chain_factory import Common
from library_chain.proof_factory import ProofFactory
from library_chain.models import Block, HashManager 
from library_chain.federated_learning import FederatedLearning
from library_chain.api import BlockRequestsSender
from library_chain.transactions import Transaction
from library_chain.transactions import TransactionPool 
from library_chain.transactions import TransactionTypes #Tipos de transacciones que permite la chain


class MainChain: 

    preprocessor = None
    identifier = 0

    def __init__(self ): 
        #self.size_per_block = size_per_block #En los nodos hoja sólo dejaremos 1 de tam
        self.chain = []
        #El dataset lo tendremos que sacar de la request que se realizará contra la blockchai de los usuarios, más concretamente, contra aquellos que sean validadores
        self.proof_cls = ProofFactory.create_proof(MainChain.identifier) #Making the Proof of learning
        self.unconfirmed_transactions = [] #No usamos una pool, las transacciones las tenemos en un array, por ahora
        self.user_chain = "" #Endpoint de la chain de los usuarios, donde tendremos las pks de las cuentas
        return

    @classmethod
    def set_user_chain(cls, user_chain  ):
        cls.user_chain = user_chain
    
    @property 
    def last_block(self ): 
        return self.chain[-1]
    
    #Solo contaremos con transacciones que lleven los enlaces y el autor (Las transacciones del resto irán en otras cadenas, por lo que no nos hace falta mirar el tipo de la cadena adjuntada)
    def check_new_transaction(self, transaction): 
        return Common.check_new_transaction( ["timestamp", "pk", "hash", "rest", "digest"   ])
   
    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction): 
        return Common.add_new_transactiokn( self, transaction )

    def add_block(self, block):
        print("REALIZAMOS LA COMRPOBACION DEL HASH")
        if self.chain[-1].hash != block.previous_hash:
            print("LA COMPROBACION DEL HASH FALLA")
            return False
        print("PASAMOS A HACER EL PROOF")
        result, model  =self.proof(block)
        print("HEMOS PASADO EL PROOF")
        if result == True: 
            block.nonce = self.proof_cls.nonce(block, self.get_dataset()) #Sacamos la precisión del bloque
            block.hash = block.get_hash() #Calculamos el hash del bloque
            block.model = model
            #Firmamos el hash del bloque con el usuario validador de la chain de usuarios
            block.signature = BlockRequestsSender.sign_leader(self.user_chain + "/sign", block.hash ) #Le pedimos a la chain que nos firme el bloque con su usuario validador
            self.chain.append(block)
            return True
        return False

    #Tenemos que llamar al request sender para que nos devuelva el dataset del usuario validador
    def get_dataset(self):
        #Sacamos el dataset en base al usuario y el endpoint
        return Common.get_dataset( self)

    #Deberemos añadir al proof en el recorrido hacia los bloques de abajo, la capacidad de coger los datasets de prueba de cada una 
    def proof(self, block ):
        #Cogemos los pesos de todos los clientes, para generar un modelo con esos pesos
        fl = FederatedLearning(model)
        model_block = fl.get_model_from_block( block)
        if( self.proof_cls.proof(self.last_block.model, model_block, self.get_dataset( ) )): 
            return True, model_block
        return False, None
    
    #Function to get a response of a prediction fronm a specific block
    def get_response_from_hash_block(self, hash, X  ): 
        return Common.get_response_from_hash_block( chain , hash ,X )
    
    #SSacamos la predicción del último bloque
    def get_response_from_last_block(self, X):
        return Common.get_resposne_from_last_block( chain ,X)
                
    #Funcion que comprueba: 
    #HASH DEL BLOQUE CALCULANDO EL NONCE 
    #PROOF DE LA PREC EN COMPARACION CON EL BLOQUE ANTERIOR
    @classmethod
    def is_valid_proof(cls, block , block_hash,  last_block ): 
        proof_cls = ProofFactory(cls.identifier).create_proof()
        block_model = NeuralModelSerializer.serialize(BlockRequestsSender.get_model_arch( block.neural_data_transaction[0]["rest"], block.neural_data_transaction[0]["hash"]))
        block_model.nonce = proof_cls.nonce(block, self.get_dataset())
        if last_block != None: 
            last_block_model = NeuralModelSerializer.serialize(BlockRequestsSender.get_model_arch( last_block.neural_data_transaction[0]["rest"], last_block.neural_data_transaction[0]["hash"]))
            if (proof_cls.proof( last_block_model, block_model, self.get_dataset() )): 
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
        return Common.get_block_by_hash(self , hash)

    def get_leader( self ): 
        return Common.get_leader( self)

    #Añadir un bloque desde los nodos
    def mine(self):
        return Common.mine(self)

    def create_genesis_block(self, wallet ):
        return Common.create_genesis_block(  self , wallet)