from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding 
from cryptography.hazmat.primitives import hashes
#from library_chain.transactions import Transaction 
from library_chain.models import HashManager

class Wallet: 

    def __init__(self , secret  ):
        secret = bytes(secret, 'utf-8') #Transformamos a Bytes para poder hacer el par de las claves
        self.balance =  0
        self.dataset_mem = None
        self.private_key_obj, self.public_key_obj = self.gen_key_pair(secret)
        self.private_key, self.public_key = self.private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(secret)
        ).hex(), self.public_key_obj.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
         ).hex()
        return
    
    def get_dataset(self ): 
        return self.dataset_mem
    
    def load_dataset( self, dataset ): 
        self.dataset_mem = dataset
        return 

    #Getting the balance of a wallet
    def getBalance(chain):
        return chain.getBalance(self.public_key)

    def gen_key_pair(self, secret ):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        return private_key, private_key.public_key()

    #To come a user validator he will need a verified dataset which will be used to validate transaction weights 
    def validator_dataset(self, dataset_filepath ): 
        self.dataset_filepath = dataset_filepath
        return

    def toString(self ):
        return {
            "Public Key": self.public_key, 
            "Balance": self.balance
        }
    
    
    #Funcion mediante la cual firmaremos una transaccion (Eliminamos nuestra pk y el digest, para que luego al hacer el verify coincide, y porque no tiene sentido) 
    def signTransaction( self, transaction ): 
        #Firmamos la transaccion quitando los parametros que no sean necesarios
        return self.sign( HashManager.get_hash( HashManager.delete_unnecesary_params_from_transaction( transaction)  ))

    def sign(self , dataHash):
        if ( type(dataHash ) != bytes): 
            dataHash = bytes(dataHash, 'utf-8')
        return self.private_key_obj.sign(
            dataHash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )    

    ''' 
    #Solo se podrán crear dos tipos de transacciones, las transacciones en las que nos hacemos validadores, por lo que habrá que incluir un dataset,
    # y las transacciones en las que añadimos unos nuevos pesos, que necesitaremos que sean validadas por un validador 
    def createTransaction( type, transaction, transaction_type, transactionPool): 
        transaction = Transaction.newTransaction(self, transaction , transaction_type )
        #Firmamos la transaccion que acabamos de añadir
        transaction.signTransaction( self, transaction )
        transactionPool.addTransaction(transaction)
        return transaction

    ''' 
    #Las transacciones las crearemos a mano
    