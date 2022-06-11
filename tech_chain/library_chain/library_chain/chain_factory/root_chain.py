from library_chain.chain_factory import Common
from library_chain.proof_factory import ProofFactory
from library_chain.api import BlockRequestsSender
from library_chain.models import Block, HashManager 
from library_chain.dataset import DatasetPreprocessor
from library_chain.neural_model_serializer import NeuralModelSerializer


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
        self.user_chain = BlockRequestsSender.chain
        print("LA CHAIN QUE TENEMOS ES")
        print(BlockRequestsSender.chain)
        print(BlockRequestsSender.chain.user_chain)
        return
    
    @property 
    def last_block(self ): 
        return self.chain[-1]
    
    #Function to get the leader validator
    def get_leader(self ):
        return Common.get_leader(BlockRequestsSender.chain) #Returns the leader address 
    
    #Checking if a transaction has the minimum values to being a blog
    def check_new_transaction(self, transaction):
        return Common.check_new_transaction( ["timestamp", "signature", "pk", "model_arch", "model_weights", "digest"], transaction)
    
    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction): 
        return Common.add_new_transaction( self, transaction )

    def add_block(self, block):
        if len( block.neural_data_transaction) > 1: 
            #Solo permitiremos que se añadan bloques con 1 transaccion
            return False 
        if self.chain[-1].hash != block.previous_hash:
            return False
        result, model  =self.proof(block)
        if result == True: 
            block.model = model
            block.nonce = self.proof_cls.nonce(block, self.get_dataset()) #Sacamos la precisión del bloque en base a los pesos del bloque y en base al dataset del validador que tenemos en la chain de los usuarios
            block.hash = block.get_hash() #Calculamos el hash del bloque
            #Le enviamos al nodo que tenemos asociado la firma del bloque que acabamos de crear
            block.signature=  BlockRequestsSender.sign_leader(BlockRequestsSender.chain.user_chain + "/sign" , block.get_hash())
            self.chain.append(block)
            self.unconfirmed_transactions.clear()
            return True
        return False

    @classmethod 
    def verify_transaction(cls, transaction ): 
        return Common.verify_signature(BlockRequestsSender.chain.user_chain, 
            transaction["signature"], 
            Common.get_hash_from_transaction( transaction) , 
            transaction["pk"]) 

    @classmethod
    def check_validity_transaction(cls, block ): 
        for i in range( 0 , len(block.neural_data_transaction)):
            if cls.verify_transaction( block.neural_data_transaction[i]) == False: 
                return False
        return True 
    
    def get_leader_by_block(self, block): 
        validators = BlockRequestsSender.get_validators( BlockRequestsSender.chain.user_chain ) #Sacamos los usuarios validadores desde nuestra chain
        #No podemos sacarlo de nuestros parametros, por lo que tendremos que enviar una req para recogerlos
        for key in validators.keys(): 
            if block.validator == key:
                return block.validator
        return None
    
    #Funciion para verificar los lideres de nuestros bloque s
    def verify_leader(self, block): 
        if self.get_leader_by_block(self, block ) != None: 
            return True
        return False

    #Comprobamos la firma del bloque 
    def verify_sign_block(self, block , leader):
        #Miramos que la firma del bloque coincida con la firma del leader 
        return Common.verify_signature(BlockRequestsSender.chain.user_chain,  block.signature, block.get_hash() , leader ) 


    def get_dataset(self ): 
        #Del dataset que hemos sacado, tendremos que realizar el preprocesado de cada uno de ellos 
        #Preprocesamos el dataset que hemos sacado del nodo para obtener un numpy arr con los datos que podamos usar pasar hallar los valores de la predicción
        print("LA CHAIN A LA QUE ESTAMOS TIRANDO ES")
        print(BlockRequestsSender.chain.user_chain + "/dataset" )
        return DatasetPreprocessor.preprocess_dataset( BlockRequestsSender.get_dataset(BlockRequestsSender.chain.user_chain + "/dataset" ) )

    #Lo tenemos que cambiar, dado que ahora el proof se realiza solamente sobre el modelo del bloque en el que nos encontramos y sobre el dataset que nos enontramos dentro del chain 
    def proof(self, block ):
        if(self.last_block.model == None ): 
            return True, NeuralModelSerializer.serialize({ "model": block.neural_data_transaction[0]["model_arch"] , "model_weights": block.neural_data_transaction[0]["model_weights"]})
        model_block = NeuralModelSerializer.serialize({ "model": block.neural_data_transaction[0]["model_arch"] , "model_weights": block.neural_data_transaction[0]["model_weights"]})
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
        block_model = NeuralModelSerializer.serialize(block.neural_data_transaction[0]["model_arch"] , block.neural_data_transaction[0]["model_weights"] )
        nonce = proof_cls.nonce(block, self.get_dataset())
        if last_block != None: 
            #Tenemos que comprobar el hash del bloque y comprobar el modelo
            block_hash_cp = HashManager.get_entire_block_hash(block)
            last_block_model = NeuralModelSerializer.serialize(last_block.neural_data_transaction[0]["model_arch"] , last_block.neural_data_transaction[0]["model_weights"] )
            if (proof_cls.proof( last_block_model, block_model , self.get_dataset())): 
                block.hash = HashManager.get_entire_block_hash( block )
                if block_hash_cp == block_hash and last_block.get_hash() == block.previous_hash and cls.check_validity_transactions( block) and  cls.verify_sign_block(cls, block , cls.get_leader_by_block(cls, block )) and cls.verify_leader( cls, block): 
                    return True
            return False
        if block_hash_cp == block_hash and cls.check_validity_transactions( block) and  cls.verify_sign_block(cls, block , cls.get_leader_by_block(cls, block )) and cls.verify_leader( cls, block): 
            print("EL PRIMER BLOQUE HA DADO POSITIVO")
            return True 
        return False 
       
    @classmethod
    def check_chain_validity(cls, chain ):
        result = True
        previous_hash = "0"
        last_block = None
        for block in chain:
            block = BlockSerializer.serialize(block)
            block_hash = block.hash
            delattr(block, "hash")
            if not cls.is_valid_proof(block, block_hash, last_block  ): 
                return False
            last_block = block
        return True

    #Function to get a block by hash
    def get_block_by_hash(self, hash): 
        return Common.get_block_by_hash( self , hash)

    #Añadir un bloque desde los nodos
    def mine(self):
        return Common.mine(self)

    def create_genesis_block(self ):
        print("ENTRAMOS EN EL GENESIS BLOCK Y NUESTRA CHAIN ES ")
        print(BlockRequestsSender.chain)
        print(BlockRequestsSender.chain.user_chain)
        genesis_block = Block(0, [], 0, "0",  self.get_leader())
        genesis_block.hash = genesis_block.get_hash()
        genesis_block.signature = BlockRequestsSender.sign_leader( BlockRequestsSender.chain.user_chain + "/sign" ,  genesis_block.get_hash())  #Firmamos la primera transaccion con la wallet principal que tenemos destinada para el nodo
        self.chain.append(genesis_block)
        return
