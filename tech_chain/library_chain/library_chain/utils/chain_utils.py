import uuid 
from library_chain.models import HashManager 
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding as Padding
from hashlib import sha256

class ChainUtils: 

    @staticmethod
    def gen_id():
        return uuid.uuid4()
    
    @staticmethod 
    def verifySignature( key , signature, hash): 
        try: 
            load_pem_public_key(key ).verify(
                signature,
                hash,
                padding.PSS(
                    mgf=padding.MGF1(sha256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                sha256()        
            )
            return 1
        except Exception as e: 
            print("ERROR: Not valid transaction")
            return 0
     
