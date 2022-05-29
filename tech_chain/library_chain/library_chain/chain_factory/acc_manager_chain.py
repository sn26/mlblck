from library_chain.staking import MiningFeature
from library_chain.transactions import TransactionPool
from library_chain.transactions import Transaction
from library_chain.transactions import TransactionTypes
from library_chain.chain_account_gen_man import Accounts
from library_chain.utils import ChainUtils
from library_chain.chain_factory import Common
from library_chain.models import Block, HashManager, BlockSerializer
from library_chain.api import BlockRequestsSender
from library_chain.proof_factory import ProofFactory


#Chain that contains user general accounts
class AccManagerChain: 

    identifier = 2 
    user_chain = None #Nodo al que nos conectaremos para sacar los datos mediante request, en realidad para esta chain no sería necesario
    def __init__(self): 
        self.chain = []
        self.unconfirmed_transactions = []
        
        self.accounts = Accounts()
        self.validators = MiningFeature( self.accounts)
        #self.user_chain = None #Solo tenemos que irnos a un nodo, y sacar de alli el leader
        return 
    
    @property 
    def last_block(self ): 
        return self.chain[-1]

    @property 
    def user_chain( self ): 
        return AccManagerChain.user_chain

    def set_user_chain( self, user_chain): 
        AccManagerChain.user_chain = user_chain #Nuestro apoyo al nodo (En realidad no hace falta para esta cad de bloques)
    
    #Function to get the leader validator
    def get_leader(self ):
        return self.validators.getMax() #Returns the leader address 

    #Function that returns the balance of an specific account
    def get_account_balance( self, pk ): 
        return self.accounts.getBalance( pk)
    
    #Verificamos que la firma del usuario correcto
    def check_new_transaction(self, transaction ): 
        
        return Common.check_new_transaction( ["fee", "dataset", "validator_endpoint_address", "transaction", "amount", "pk", "signature", "timestamp", "to", "digest"], transaction )

    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction):  
        #Cuando pasamos a añadir una nueva transaccion, verificamos que sea correcta la firma
        return Common.add_new_transaction( self, transaction)
    
    #Cuando añadimos un bloque a nuestra chain, tendremos que actualizadar los nodos validadores y las cuentas de cada uno de nuestros nodos
    def execute_block( self): 
        print("ESTAMOS PASANDO A EJECUTAR EL BLOQUE" )
        for itransact in  self.last_block.neural_data_transaction: 
            print("ESTAMOS ENTRANDO A EJECUTAR EL BLOQUE")
            print( itransact["transaction"])
            print(TransactionTypes.VALIDATOR)
            if itransact["transaction"] == TransactionTypes.VALIDATOR:
                print("HEMOS ENTRANDO A AÑADIR UN VALIDADOR")
                self.accounts.add_address(itransact["pk"])
                self.validators.update(itransact)
            elif itransact["transaction"] == TransactionTypes.ADDSTAKE: 
                self.accounts.add_address(itransact["pk"])
                self.validators.addStake( itransact["pk"], 
                itransact["amount"] )

            elif itransact["transaction" ] == TransactionTypes.ADDVALDATASTAKE: 
                self.validators.addValidationData( itransact["pk"], itransact["dataset"])
            elif itransact["transaction"] == TransactionTypes.ADDADDRESS: 
                self.accounts.add_address(itransact["pk"]) #Añadimos una nuevacuenta con balance 0
            elif itransact["transaction"] == TransactionTypes.ADDTRANSACTION: 
                self.accounts.transfer(itransact["pk"], itransact["to"], itransact["amount"])
        return

    #METODOS PARA REALIZAR EL PROOF DE LAS CADENAS
    def proof(self, block ): 
        #Nuestro proof consistirá en firmar el bloque con el validador 
        if self.get_leader( ) != None: 
            #Comprobamos todas las transacciones que irán dentro del bloque, para saber si es correcto o no lo es 
            return self.check_validity_transactions(block)
        return False
    
    #Funcion mediante la cual verificamos una transacción (Verificamos que sea correcta la firma de la transaccion, a lo mejor lo deberiamos de cambiar a transacciones)
    @classmethod 
    def verify_transaction(cls , transaction):
        
        return Common.verify_signature(AccManagerChain.user_chain, transaction["signature"], Common.get_hash_from_transaction( transaction) , transaction["pk"]) 

    @classmethod
    #Funcion mediante la cual validamos las transacciones de nuestro bloque
    def check_validity_transactions(cls , block): 
        for i in range( 0 ,  len(block.neural_data_transaction )): 
            if cls.verify_transaction( block.neural_data_transaction[i]) == False: 
                return False
        return True 

    #Comprobamos que el que firmó el bloque se encuentre entre nuestros validadores
    def get_leader_by_block(self, block): 

        validators = BlockRequestsSender.get_validators( AccManagerChain.user_chain ) #Sacamos los usuarios validadores desde nuestra chain
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
        return Common.verify_signature(AccManagerChain.user_chain,  block.signature, block.get_hash() , leader ) 

    @classmethod
    def is_valid_proof(cls, block, block_hash, last_block): 
        #last_block -> Bloque anterior al lanterior 
        #block -> Bloque que me viene de la otra chain
        #PARA LA BLOCKCHAIN DE LOS USERS NO SE HACE UN POL 
        #proof_cls =ProofFactory(cls.identifier).create_proof()
        
        if last_block != None: 
            #if( proof_cls.proof( last_block , block)):
            block_hash_cp = HashManager.get_entire_block_hash( block)
            print("ESTAMOS ENTRANDO EN EL RESTO DE LOS BLOQUES")
            print( block_hash_cp)
            print(block_hash)
            print(block_hash_cp == block_hash)
            print(last_block.get_hash() == block.previous_hash)
            print(cls.check_validity_transactions( block) )
            print(cls.verify_sign_block(cls, block , cls.get_leader_by_block(cls, block )))
            print(cls.verify_leader( cls, block))
            if block_hash_cp == block_hash and last_block.get_hash() == block.previous_hash and cls.check_validity_transactions( block) and  cls.verify_sign_block(cls, block , cls.get_leader_by_block(cls, block )) and cls.verify_leader( cls, block): 
                return True
        block_hash_cp = HashManager.get_entire_block_hash(block)
        #Si el bloque ha sido firmado correctamente, y ha sido firmado por un leader, lo daremos por bueno
        if block_hash_cp == block_hash and cls.check_validity_transactions( block) and  cls.verify_sign_block(cls, block , cls.get_leader_by_block(cls, block )) and cls.verify_leader( cls, block): 
            print("EL PRIMER BLOQUE HA DADO POSITIVO")
            return True 
        return False 

    @classmethod
    def check_chain_validity(cls, chain): 
        result = True
        previous_hash ="0"
        last_block = None 
        for block in chain: 
            print("El bloque que estamos probando es ")
            block = BlockSerializer.serialize(block) #Serializamos el bloque para poder utilizarlo como obj
            print(block.to_string())
            block_hash = block.hash
            delattr(block, "hash")
            print("El bloque hash es ")
            print(block_hash)
            #En el valid proof estamos comprobando el bloque, con el bloque anterior al bloque comprobado, pero de la misma chain
            if not cls.is_valid_proof( block , block_hash , last_block ):
                print("EL PROOF HA DADO NEGATIVO")
                return False 
            last_block= block
        return True
    
    def add_block(self, block): 
        if self.chain[-1].hash != block.previous_hash:
            return False
        result = self.proof( block)
        if result == True: 
            block.nonce = self.validators.getNonce() #En realidad este valor nos das un poco igual 
            
            block.model = None 
            block.hash = block.get_hash()
            block.signature =  HashManager.encode_signature( BlockRequestsSender.sign_leader( AccManagerChain.user_chain  + "/sign", block.get_hash( )) )
            print( block.to_string( ))
            self.chain.append(block)
            #Una vez hemos añadido el bloque, pasamos a ejecutarlo

            self.execute_block( )
            self.unconfirmed_transactions.clear() #Limpiamos las transacciones 
            return True
        return False 


    #Sacamos los bloques
    #Añadir un bloque desde los nodos
    def mine(self ): 
        return Common.mine(self)

    def create_genesis_block( self , wallet): 
        return Common.create_genesis_block( self , wallet)