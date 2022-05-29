from library_chain.api import BlockRequestsSender
import time 
from library_chain.utils import ChainUtils
from library_chain.models import Block, HashManager
import base64
import copy

#Class that contains common chains funcionalities between chains
class Common: 
    

    #Para cada nueva transaccion, se comprobaran los campos y la firma
    #Tambien se comprobará la firma de la transaccion
    @staticmethod
    def check_new_transaction( keys, transaction ): 
        for key in transaction.keys(): 
            if key not in keys: 
                print( "ERROR 400: Not Valid Keys ") 
                print(keys) 
                return False
        return True

    #Comprobamos la firma en base al hash, la pk del que ha firmado y contra el endpoint de la chain de los usuarios
    @staticmethod
    def verify_signature(  user_chain, signature , hash , pk ):
        if  type(signature) != bytes: 
            #Si nos han pasado una firma que está en b64 
            signature = HashManager.decode_signature(signature)
        return ChainUtils.verify_signature(pk, signature, hash )
        #return BlockRequestsSender.verify_signature( user_chain , signature, hash , pk) 

    @staticmethod
    def get_hash_from_transaction( transaction ): 
        return HashManager.get_hash(HashManager.delete_unnecesary_params_from_transaction(transaction))

    @staticmethod 
    def add_new_transaction( chain , transaction): 
        if chain.check_new_transaction(transaction): 
            if Common.verify_signature(chain.user_chain, transaction["signature"], Common.get_hash_from_transaction( transaction) , transaction["pk"]) == True: 
                transaction["digest"] = Common.get_hash_from_transaction( transaction) #Meteremos el hash de la transaccion
                if type(transaction["signature"]) == bytes: 
                    transaction["signature"] = HashManager.encode_signature(transaction["signature"]) #Codificamos a b64 la firma
                chain.unconfirmed_transactions.append(transaction)
                return True 
        return False

    @staticmethod
    def get_dataset( chain ): 
        return BlockRequestsSender.get_dataset(chain.user_chain + '/dataset')

    @staticmethod 
    def get_response_from_last_block( chain , X): 
        return str( chain.last_block.model.predict(X).argmax(axis=1)[0] )

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
        return BlockRequestsSender.get_leader( chain.user_chain + "/get_leader") #Sacamos el leader

    #Añadir un bloque desde los nodos
    @staticmethod
    def mine(chain):
        if len(chain.unconfirmed_transactions) == 0 : 
            print("ERROR: There aren't transactions to Mine")
            return False
        last_block = chain.last_block
        new_block = Block(index=last_block.index + 1,
                        transactions=copy.deepcopy(chain.unconfirmed_transactions ),
                        timestamp=time.time(),
                        previous_hash=copy.deepcopy(last_block.hash),  #Si no hacemos un deep copy, luego no podremos borrar las transacciones
                        validator= chain.get_leader())
        return chain.add_block(new_block)  

    @staticmethod
    def create_genesis_block(chain, wallet ):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0", wallet.public_key)
        genesis_block.hash = genesis_block.get_hash()
        genesis_block.signature = HashManager.encode_signature(  wallet.sign( genesis_block.get_hash()) ) #Firmamos la primera transaccion con la wallet principal que tenemos destinada para el nodo
        chain.chain.append(genesis_block)
        return