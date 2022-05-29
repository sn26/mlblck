from library_client.api import LogImgGenerator 
from library_client.api import ClientRequestSender 
import base64 
import gzip 
import json 
import os

#Cliente que usaremos para realizar las requests contra nuestro conj de chains
class ClientServiceSender: 

    #Necesitaremos añadir una Wallet que se usará para el cliente
    def __init__(self, host, wallet ):
        self.host =host
        self.clr_sender = ClientRequestSender(host)
        #self.log_img_gen = LogImgGenerator( )
        self.wallet = wallet 
        return

    def generate_encoded_transaction_and_signature_for_test(self, transaction  ): 
        signature = base64.encodebytes( self.wallet.signTransaction( transaction ) ).decode("utf-8")
        #codificamos la transaccion y la firma
        res = base64.encodebytes( bytes( json.dumps( str( transaction))  , "utf-8" ) ).decode("utf-8")
        compression = gzip.compress( bytes ( json.dumps( res) , "utf-8" )  )
        return base64.encodebytes( compression).decode("utf-8"), signature


    #Funcion que usaremos para añadir una validador y datos para ese validador
    def add_validator(self, amount, fee   ): 
        transaction = {"fee": fee  , "amount":amount  ,
            "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
            "to": "0", "digest": 0, "validator_endpoint_address": "http://" + self.host , "dataset": [] }
        res, signature= self.generate_encoded_transaction_and_signature_for_test( transaction ) 
        return self.clr_sender.add_validator( res , signature  ) #Enviamos la peticion para ser un validador 

    #Intentamos minar las transacciones que hayamos añadido 
    def mine( self ): 
        return self.clr_sender.mine( )

    def add_data_to_stake(self, file ): 
        #Añadimos la data de la que vamos a hacer stake 
        self.valdata =  LogImgGenerator.read_one_file( file) #Añadimos los datos al json de la validacion
        return 
    
    def send_data_to_stake(self , amount , fee  ): 
        transaction = {"fee":fee , "amount": amount  ,
            "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
            "to": "0", "digest": 0, "dataset": self.valdata  } #Nuestra val data es un diccionario con las imgs en b64 de cada una 
        res, signature= self.generate_encoded_transaction_and_signature_for_test( transaction )
        return self.clr_sender.add_data(  res , signature ) #Enviamos la peticion para ser un validador 

    def add_account(self): 
        transaction = {"fee": 0  , "amount": 0 ,
         "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
          "to": self.wallet.public_key , "digest": 0 }
        res, signature = self.generate_encoded_transaction_and_signature_for_test( transaction )
        return self.clr_sender.add_account( res, signature)

   
    