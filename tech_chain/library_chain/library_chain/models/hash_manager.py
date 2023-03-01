from hashlib import sha256
import json
import copy 
import base64
from library_chain.service_tools import ServiceTools

class HashManager: 

    #Metodo para comprobar si la firma está en bsae64 o si la tenemos en bytes (Aunque todas deberían estar en b64)
    @staticmethod
    def isBase64(sb):
        try:
            if isinstance(sb, str):
                # If there's any unicode here, an exception will be thrown and the function will return false
                sb_bytes = bytes(sb, 'utf-8')
            elif isinstance(sb, bytes):
                sb_bytes = sb
            else:
                raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
        except Exception:
                return False


    #Funcion para codificar las firmas en b64 (Necesario para poder pasarlo por las requests)
    @staticmethod
    def encode_signature( signature):
        #Codificamoso en base 64 la firma
        if type(signature ) !=  bytes: 
            return signature
        if HashManager.isBase64( signature ) == True : return signature
        return base64.encodebytes(  signature ).decode("utf-8")

    #Funcion para decodificar las firmas 
    @staticmethod 
    def decode_signature( signature):  
        try: 
            return ServiceTools.decode_signature( signature) 
        except Exception as e: 
            if HashManager.isBase64( signature ) != True: 
                return signature

    #Sacamos los hahshes de cada uno de los datos del bloque 
    @staticmethod
    def root_node_hashes(transactions): 
        root_hashes = []
        for i in range(0, len(transactions)): 
            root_hashes.append( HashManager.get_hash(transactions[i]) ) 
        return root_hashes

    #Funcion para borrar as calves/ valores de una transaccion que no sean necesarios 
    @staticmethod 
    def delete_unnecesary_params_from_transaction(transaction ): 
        transactioncp = copy.deepcopy( transaction )
        try: 
            del transactioncp["digest"]
        except Exception as e: 
            pass 
        try: 
            del transactioncp["signature"]
        except Exception as e: 
            pass
        try: 
            del transactioncp["timestamp"]
        except Exception as e: 
            pass
        #Despues de las pruebas lo tendremos que quitar para mayor fiabilidad del sistema
        try: 
            del transactioncp["transaction"]
        except Exception as e: 
            pass
        return transactioncp
    
    @staticmethod
    def get_in_pairs( hashes): 
        if (len(hashes ) == 1 or len(hashes ) ==  0 ): 
            if type(hashes ) == list and len(hashes) != 0: 
                return hashes[0]
            return hashes
        if ( len(hashes) == 2):
            return HashManager.get_hash(hashes)
        result = []  
        counter = 0 
        for i in range(0, len(hashes) - 1): 
            i = counter
            if i < len(hashes ) -1: 
                result.append( HashManager.get_in_pairs([ hashes[i], hashes[i+1 ]]))
            elif i == len(hashes ) -1: 
                result.append(hashes[i])
                return HashManager.get_in_pairs(result)
            counter = counter + 1 + 1 
        return HashManager.get_in_pairs(result)

    @staticmethod
    def gen_hash_tree(transactions ): 
        return HashManager.get_in_pairs(HashManager.root_node_hashes(transactions))
    
    @staticmethod
    def get_hash(transaction):
        try: 
            return sha256(json.dumps(transaction , sort_keys= True).encode()).hexdigest()
        except: 
            print("ERROR: Incorrect Transaction " )
            print(transaction )
            return sha256( json.dumps({}, sort_keys=True).encode( )).hexdigest( )

    @staticmethod
    #Function that calculate the hash from one transaction in a whole block
    def get_entire_block_hash( block ): 
        
        data = list([block.timestamp, block.index, block.nonce, block.previous_hash, HashManager.gen_hash_tree(block.neural_data_transaction) , block.model_to_string() ])
        return HashManager.get_hash(data)
