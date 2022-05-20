import uuid 
from library_chain.models import HashManager 
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class ChainUtils: 

    @staticmethod
    def gen_id():
        return uuid.uuid4()
    
    @staticmethod 
    def verify_signature( key , signature, hash): 
        try:
            if type(key) == str: 
                key = bytearray.fromhex(key)
            if (type(signature) != bytes): 
                signature = bytes( signature, 'utf-8')
            if( type(hash) != bytes ): 
                hash = bytes( hash , 'utf-8')
            try: 
                pk =load_pem_public_key(key )
                pk.verify(
                    signature,
                    hash,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()      
                )
                return True
            except Exception as e: 
                print(e)
                print("ERROR 500: Invalid Signature, Not valid transaction!")
                return False
        except Exception as e: 
            #Si no hemos conseguido hacer un casting de la firma
            print(e)
            print("ERROR 500: Invalid Signature, Not valid transaction!")
            return False
