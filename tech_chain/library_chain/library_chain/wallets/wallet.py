from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding 
from cryptography.hazmat.primitives import hashes
#from library_chain.transactions import Transactionf
from library_chain.models import HashManager
import json

class Wallet: 

    def __init__(self , secret  ):
        self.secret = secret 
        self.balance =  0
        self.dataset_mem = None
        self.private_key_obj, self.public_key_obj = self.gen_key_pair()
        self.private_key, self.public_key = self.get_hex_pair( self.private_key_obj, self.public_key_obj, secret)
        return
    
    def set_chain_wallet( self, file_path ): #Aunque otro nodo establezca su wallet aqui como adm, esta será rechazada en el consenso por el resto de nodos
        #Serializamos la clave publica y la privada, respecto a las que tenemos nosotros dentro de nuestra chain
        # Opening JSON file
        f = open(file_path) #En el resto de los nodos, no pasaremos ni la private key ni la password
        # returns JSON object as 
        # a dictionary
        adm = json.load(f)
        #Nos da igual el secret que pongamos porque se lo vamos a cambiar con el file
        self.private_key_obj = self.serialize_private_key_from_hex(adm["private_key"], adm["password"])
        self.public_key_obj = self.serialize_public_key_from_hex( adm["public_key"])
        self.private_key, self.public_key = self.get_hex_pair(self.private_key_obj  , self.public_key_obj, adm["password"])
        return self
    
    def get_hex_pair( self , private_key_obj, public_key_obj, secret):
        return private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(bytes(secret, 'utf-8'))
        ).hex(), public_key_obj.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
         ).hex()

    def get_dataset(self ): 
        return self.dataset_mem
    
    def load_dataset( self, dataset ): 
        self.dataset_mem = dataset
        return 

    #Funcion que nos permite serializar la clave de entrada dado un conjunto hexadecimal
    def serialize_private_key_from_hex(self, data, password ): 
        return serialization.load_pem_private_key(bytes( bytearray.fromhex(data) ), bytes( password , "utf-8") ) #Devolvemos la clave serializada

    def serialize_public_key_from_hex(self, data):
        return serialization.load_pem_public_key(bytes(bytearray.fromhex(data)))

    #Getting the balance of a wallet
    def getBalance(chain):
        return chain.getBalance(self.public_key)

    def gen_key_pair(self):
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
    