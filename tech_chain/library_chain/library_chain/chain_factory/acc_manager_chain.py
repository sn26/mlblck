from library_chain.staking import MiningFeature
from library_chain.transactions import TransactionPool
from library_chain.transactions import Transaction
from library_chain.transactions import TransactionTypes
from library_chain.chain_account_gen_man import Account
from library_chain.utils import ChainUtils
from library_chain.chain_factory import Common

#Chain that contains user general accounts
class AccManagerChain: 

    identifier = 2 

    def __init__(self): 
        self.chain = []
        self.unconfirmed_transactions = []
        self.validators = MiningFeature( )
        self.accounts = Accounts()
        return 
    
    #Function to get the leader validator
    def get_validator(self ): 
        return self.validators.getMax() #Returns the leader address 

    #Function that returns the balance of an specific account
    def get_account_balance( self, pk ): 
        return self.accounts.getBalance( pk)
    
    #Verificamos que la firma del usuario correcto
    def check_new_transaction(self, transaction ): 
        return Common.check_new_transaction( ["fee", "transaction", "amount", "pk", "signature", "timestamp", "to", "digest"], transaction )

    #Si el check ha sido correcto, añadiremos la transaccion al conjunto de transacciones que aun no se han realizado
    def add_new_transaction(self, transaction):  
        #Cuando pasamos a añadir una nueva transaccion, verificamos que sea correcta la firma
        return Common.add_new_transaction( self, transaction)
    
    #Cuando añadimos un bloque a nuestra chain, tendremos que actualizadar los nodos validadores y las cuentas de cada uno de nuestros nodos
    def execute_block( self): 
        for itransact in  self.last_block().neural_data_transaction: 
            
            if itransact["transaction"] == "new_validator":
                self.accounts.add_address(itransact["pk"])
                self.validators.update(itransact)
            elif itransact["transaction"] == "addStake": 
                self.accounts.add_address(itransact["pk"])
                self.validators.addStake( itransact["pk"], 
                itransact["amount"] )

            elif itransact["transaction" ] == "addValDataStake": 
                self.validators.addValidationData( itransact["pk"], itransact["dataset"])
            elif itransact["transaction"] == "addAddress": 
                self.accounts.add_address(itransact["pk"]) #Añadimos una nuevacuenta con balance 0
            elif itransact["transaction"] == "transaction": 
                self.accounts.transfer(itransact["pk"], itransact["to"], itransact["amount"])
        return

    #METODOS PARA REALIZAR EL PROOF DE LAS CADENAS
    def proof(self, block ): 
        #Nuestro proof consistirá en firmar el bloque con el validador 
        if self.get_validator( ) != None: 
            #Comprobamos todas las transacciones que irán dentro del bloque, para saber si es correcto o no lo es 
            return self.check_validity_transactions(block)
        return False
    
    #Funcion mediante la cual verificamos una transacción (Verificamos que sea correcta la firma de la transaccion, a lo mejor lo deberiamos de cambiar a transacciones)
    def verifyTransaction(transaction): 
        return  ChainUtils.verifySignature(  
            transaction["from"], 
            transaction["signature"], 
            HashManager.get_hash(transaction.output)
        )

    #Funcion mediante la cual validamos las transacciones de nuestro bloque
    def check_validity_transactions(self , block): 
        for i in range( 0 ,  len(block.transactions )): 
            if self.verifyTransaction( block.transactions[i]) == False: 
                return False
            return True 


    #Comprobamos que el que firmó el bloque se encuentre entre nuestros validadores
    def get_leader_by_block(self, block): 
        for i in range(self.validators.validators ): 
            if block.validator == self.validators.validators[i]:
                return self.validators.validators[i]
        return None
    
    #Funciion para verificar los lideres de nuestros bloque s
    def verify_leader(self, block): 
        if self.getLeaderbyBlock( block ) != None: 
            return True
        return False
    

    #Comprobamos la firma del bloque 
    def verifySignBlock(self, block , leader):
        #Miramos que la firma del bloque coincida con la firma del leader 
        if ChainUtils.verifySignature( leader , block.signature, block.hash ) == 1: 
            return True
        return False


    @classmethod
    def is_valid_proof(cls, block, block_hash, last_block): 
        proof_cls =ProofFactory(cls.identifier).create_proof()
        if last_block != None: 
            if( proof_cls.proof( last_block , block)):
                block.hash = HashManager.get_entire_block_hash( block)
                if block.hash == block_hash and last_block.hash == block.previous_hash and cls.checK_validity_transactions(block) and cls.verifyBlock(block ) and cls.verifyLeader( block, cls.getLeader()): 
                    return True
        block.hash = HashManager.get_entire_block_hash(block)
        #Si el bloque ha sido firmado correctamente, y ha sido firmado por un leader, lo daremos por bueno
        if block.hash == block_hash and cls.checK_validity_transactions(block) and  cls.verifySignBlock(block , cls.getLeaderByBlock()) and cls.verifyLeader( block, cls.getLeader()): 
            return True 
        return False 

    @classmethod
    def check_chain_validity(cls, chain): 
        result = True
        previous_hash ="0"
        last_block = None 
        for block in chain: 
            block_hash = block.hash
            delattr(block, "hash")
            if not cls.is_valid_proof(block , block_hash , last_block ) or last_block.hash != block.previous_hash:
                return False 
            last_block= block
        return True
    
    def add_block(self, block): 
        if self.chain[-1].hash != block.previous_hash: 
            return False
        result = self.proof( block)
        if result == True: 
            block.nonce = self.validators.getNonce() #En realidad este valor nos das un poco igual 
            block.hash = block.set_hash()
            block.model = None 
            block.signature = BlockRequestSender.sign_leader( self.user_chain  + "/sign")
            self.chain.append(block)
            #Una vez hemos añadido el bloque, pasamos a ejecutarlo
            self.execute_block( )
            return True
        return False 


    #Sacamos los bloques
    #Añadir un bloque desde los nodos
    def mine(self ): 
        return Common.mine(self)

    def create_genesis_block( self): 
        return Common.create_genesis_block( self)