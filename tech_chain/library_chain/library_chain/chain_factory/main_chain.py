from library_chain.chain_factory import Common
from library_chain.proof_factory import ProofFactory
from library_chain.models import Block, HashManager 
from library_chain.federated_learning import FederatedLearning
from library_chain.api import BlockRequestsSender
from library_chain.dataset import DatasetPreprocessor
from library_chain.neural_model_serializer import NeuralModelSerializer
import tensorflow_federated as tff
import tensorflow as tf

class MainChain: 

    identifier = 0

    def __init__(self ): 
        #self.size_per_block = size_per_block #En los nodos hoja sólo dejaremos 1 de tam
        self.chain = []
        #El dataset lo tendremos que sacar de la request que se realizará contra la blockchai de los usuarios, más concretamente, contra aquellos que sean validadores
        self.proof_cls = ProofFactory.create_proof(MainChain.identifier) #Making the Proof of learning
        self.unconfirmed_transactions = [] #No usamos una pool, las transacciones las tenemos en un array, por ahora
        self.user_chain = BlockRequestsSender.chain #Endpoint de la chain de los usuarios, donde tendremos las pks de las cuentas
        return

    @property 
    def last_block(self ): 
        return self.chain[-1]
    
      #Function to get the leader validator
    def get_leader(self ):
        return Common.get_leader(BlockRequestsSender.chain) #Returns the leader address 

    #Solo contaremos con transacciones que lleven los enlaces y el autor (Las transacciones del resto irán en otras cadenas, por lo que no nos hace falta mirar el tipo de la cadena adjuntada)
    def check_new_transaction(self, transaction): 
        return Common.check_new_transaction( ["timestamp", "pk", "signature", "digest", "rest_federated_blocks"   ], transaction)
   
    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction): 
        return Common.add_new_transaction( self, transaction )

    def add_block(self, block):
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

    #Tenemos que llamar al request sender para que nos devuelva el dataset del usuario validador
    def get_dataset(self):
        #Sacamos el dataset en base al usuario y el endpoint
        #Devolvemos el dataset formatedo en tf 
        return DatasetPreprocessor.preprocess_dataset( BlockRequestsSender.get_dataset(BlockRequestsSender.chain.user_chain + "/dataset" ) )
        #return tf.data.Dataset.from_tensor_slices((dataset["x_test"], dataset["y_test"]))
      

    #Deberemos añadir al proof en el recorrido hacia los bloques de abajo, la capacidad de coger los datasets de prueba de cada una 
    def proof(self, block ):
        dataset = self.get_dataset( )
        model = FederatedLearning.federated_neural_model_serializer(block, dataset)
        #CAMBIAMOS LOS TIPOS
        #FederatedLearning.federated_server_type = tff.FederatedType(model.trainable_variables.type_signature.result, tff.SERVER)
        #FederatedLearning.federated_dataset_type = tff.FederatedType(tff.SequenceType(model.input_spec) , tff.CLIENTS)
        #SACAMOS LOS PESOS Y SETEAMOS LOS PESOS EN EL MODELO QUE VAMOS A COMPROBAR
        #mcwghts = FederatedLearning.get_mean_client_weights(client_wghts, clients_total) #Sacamos la media de los pesos
        #model.set_weights( FederatedLearning.server_update(model, mcwghts) ) 
        if(self.last_block.model == None ): 
            print("EL MODELO QUE ESTAMOS DEVOLVIENDO ES ")
            print( model.to_json())
            return True, model
        #model_block =  FederatedLearning.get_model_from_block( block)
        if( self.proof_cls.proof(self.last_block.model,model, dataset )): 
            return True,  model
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
        proof_cls = ProofFactory(MainChain.identifier).create_proof()
        block.model = FederatedLearning.get_model_from_block(block)
        nonce = proof_cls.nonce(block, self.get_dataset())
        if last_block != None: 
            #Tenemos que comprobar el hash del bloque y comprobar el modelo
            block_hash_cp = HashManager.get_entire_block_hash(block)
            last_block_model = FederatedLearning.get_model_from_block(last_block)
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
        return Common.get_block_by_hash(self , hash)

    #Añadir un bloque desde los nodos
    def mine(self):
        return Common.mine(self)

    def create_genesis_block(self  ):
        print("ENTRAMOS EN EL GENESIS BLOCK Y NUESTRA CHAIN ES ")
        print(BlockRequestsSender.chain)
        print(BlockRequestsSender.chain.user_chain)
        genesis_block = Block(0, [], 0, "0",  self.get_leader())
        genesis_block.hash = genesis_block.get_hash()
        genesis_block.signature = BlockRequestsSender.sign_leader( BlockRequestsSender.chain.user_chain + "/sign" ,  genesis_block.get_hash())  #Firmamos la primera transaccion con la wallet principal que tenemos destinada para el nodo
        self.chain.append(genesis_block)
        return