from library_client_chain.api import LogChainImgGenerator 
from library_client_chain.api import ClientChainRequestSender 
from library_client_chain.model_serializer import ModelSerializer
import base64 
import gzip 
import json 
import os
import pickle
#Cliente que usaremos para realizar las requests contra nuestro conj de chains
class ClientServiceSender: 

    #Necesitaremos añadir una Wallet que se usará para el cliente
    def __init__(self, host, wallet ):
        self.host =host
        self.clr_sender = ClientChainRequestSender(host)
        #self.log_img_gen = LogChainImgGenerator ( )
        self.wallet = wallet 
        return

    def set_host(self ,host):
        self.host = host
        self.clr_sender.set_host(host)
        return     
    
    def get_host(self ): 
        return self.host
    

    def generate_encoded_transaction_and_signature(self, transaction  ): 
        signature = base64.encodebytes( self.wallet.signTransaction( transaction ) ).decode("utf-8")
        #codificamos la transaccion y la firma
        res = base64.encodebytes( bytes( json.dumps( str( transaction))  , "utf-8" ) ).decode("utf-8")
        compression = gzip.compress( bytes ( json.dumps( res) , "utf-8" )  )
        return base64.encodebytes( compression).decode("utf-8"), signature

    def get_parsed_model_weight(self , model_weights):
        json_data= {}
        for i in range(0 , len( model_weights)): 
            json_data["n" + str(i)] =   base64.encodebytes(  model_weights[i].tobytes()  ).decode("utf-8")
            json_data["shape n" + str(i)] =  base64.encodebytes(bytes( json.dumps( str( model_weights[i].shape))  , "utf-8" ) ).decode("utf-8")
            
        return json_data
    
    def get_parsed_rest_blocks(self, list_node_hashes): 
        json_data= {}
        for i in range(0 , len( list_node_hashes)): 
            json_data["rest" + str(i)] =   base64.encodebytes( bytes( json.dumps( str( list_node_hashes[i]["rest"]))  , "utf-8" )).decode("utf-8")
            json_data["hash" + str(i)] =  base64.encodebytes(bytes( json.dumps( str( list_node_hashes[i]["hash"]))  , "utf-8" ) ).decode("utf-8")
        return json_data

    
    
    ############################################################
    ############################################################
    #CONJUNTO DE FUNCIONES QUE VAMOS A USAR PARA LA MAIN CHAIN
    ############################################################
    ############################################################

    def send_main_federated_transaction( self, list_node_hashes):
        #Serializamos el modelo, para poder pasarlo a la chain de manera sencilla
        print("EL NODO QUE ESTAMOS ENVIANDO ES ")
        print(list_node_hashes)
        parsed_nodes = self.generate_encoded_transaction_and_signature(  self.get_parsed_rest_blocks(list_node_hashes) )[0]
        transaction = {"rest_federated_blocks": parsed_nodes,
            "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
            "digest": 0 }
        print("LA TRANSACCION FINAL ES ")
        print(transaction)
        signature= self.generate_encoded_transaction_and_signature( transaction )[1]
        transaction["rest_federated_blocks"] = []
        res =  self.generate_encoded_transaction_and_signature( transaction )[0]
        return self.clr_sender.send_main_model_transaction( res , parsed_nodes,  signature)

    ############################################################
    ############################################################
    #CONJUNTO DE FUNCIONES QUE VAMOS A USAR PARA LA ROOT CHAIN
    ############################################################
    ############################################################
    #Model_arch: File que contiene el json con la estructura del modelo definida
    # Model_weights: File que contiene los pesos del modelo    
    def send_root_model_transaction( self, file_model_arch , file_model_weights ):
        #Serializamos el modelo, para poder pasarlo a la chain de manera sencilla
        model = ModelSerializer.serialize(json.load(open(file_model_arch)) , file_model_weights)
        print("EL MODELO QUE ESTAMOS RECOGIENDO ES")
        print(type( model.get_weights()))
        model_weights = self.generate_encoded_transaction_and_signature( self.get_parsed_model_weight( model.get_weights()) )[0] #self.generate_encoded_transaction_and_signature(model.get_weights())[0]
        model_arch = self.generate_encoded_transaction_and_signature(model.to_json() )[0]
        transaction = {"model_arch": model_arch  , "model_weights": model_weights  ,
            "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
           "digest": 0 }
        print("LA TRANSACCION FINAL ES ")
        print(transaction)
        signature= self.generate_encoded_transaction_and_signature( transaction )[1]
        transaction["model_arch"] = []
        transaction["model_weights"] = []
        res =  self.generate_encoded_transaction_and_signature( transaction )[0]
        return self.clr_sender.send_root_model_transaction( res ,model_arch, model_weights,  signature)
        



    ############################################################
    ############################################################
    #CONJUNTO DE FUNCIONES QUE VAMOS A USAR PARA LA ACC CHAIN 
    ############################################################
    ############################################################


    #Funcion que usaremos para añadir una validador y datos para ese validador
    def add_validator(self, amount, fee, host, port    ): 
        transaction = {"fee": fee  , "amount":amount  ,
            "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
            "to": "0", "digest": 0, "validator_endpoint_address": "http://" + host + ":" + port, "dataset": [] }
        res, signature= self.generate_encoded_transaction_and_signature( transaction ) 
        return self.clr_sender.add_validator( res , signature  ) #Enviamos la peticion para ser un validador 

    #Intentamos minar las transacciones que hayamos añadido 
    def mine( self ): 
        return self.clr_sender.mine( )

    def add_data_to_stake(self, file ): 
        #Añadimos la data de la que vamos a hacer stake 
        self.valdata =  LogChainImgGenerator.read_one_file( file) #Añadimos los datos al json de la validacion
        return self.valdata 
    
    def send_data_to_stake(self , amount , fee  ): 
        transaction = {"fee":fee , "amount": amount  ,
            "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
            "to": "0", "digest": 0, "dataset":self.valdata } #Nuestra val data es un diccionario con las imgs en b64 de cada una 
        signature= self.generate_encoded_transaction_and_signature( transaction )[1]
        transaction["dataset"] = []
        res =  self.generate_encoded_transaction_and_signature( transaction )[0]
        print("LOS DATOS QUE VAMOS A MANDAR SON")
        print( res)
        print("EL DATASET QUE TENEMOS DE ENTRADA ES")
        print(self.valdata)
        return self.clr_sender.add_data(  res , signature , json.dumps( self.valdata))  #Enviamos la peticion para ser un validador 

    def add_account(self): 
        transaction = {"fee": 0  , "amount": 0 ,
         "pk": self.wallet.public_key, "signature":"0" , "timestamp": 0 ,
          "to": self.wallet.public_key , "digest": 0 }
        res, signature = self.generate_encoded_transaction_and_signature( transaction )
        return self.clr_sender.add_account( res, signature)

    def ico(self): 
        return self.clr_sender.ico( self.wallet.public_key )
   
    