import requests 

#Class to send rquest to the cnn server 
class ClientChainRequestSender():
    
    def __init__(self , host):
        self.host = host
        return
    
    def set_host(self , host): 
        self.host = host
        return 
    
    def get_host(self, host): 
        return self.host
    
    
    ############################################################
    ############################################################
    #CONJUNTO DE FUNCIONES QUE VAMOS A USAR PARA LA MAIN CHAIN
    ############################################################
    ############################################################

    def send_main_model_transaction(self,  data ,list_node_hashes,  signature):
        #Enviaremos los modelos por separado de la transaccion en b64
        return requests.post( "http://" + self.host + "/new_federated_lerning_model" , data=  {
            "transaction_b64": data , 
            "rest_federated_blocks": list_node_hashes, 
            "signature": signature
        }).content  

    ############################################################
    ############################################################
    #CONJUNTO DE FUNCIONES QUE VAMOS A USAR PARA LA ROOT CHAIN
    ############################################################
    ############################################################

    def send_root_model_transaction(self, data,model_arch, model_weights,  signature):
        #Enviaremos los modelos por separado de la transaccion en b64
        return requests.post( "http://" + self.host + "/new_model" , data=  {
            "transaction_b64": data , 
            "model_weights": model_weights, 
            "model_arch": model_arch,
            "signature": signature
        }).content    



    ############################################################
    ############################################################
    #CONJUNTO DE FUNCIONES QUE VAMOS A USAR PARA LA ACC CHAIN 
    ############################################################
    ############################################################



    #Funcion que manda una request para añadir un validador 
    def add_validator(self, data, signature ):
        return requests.post( "http://" + self.host + "/new_validator" , data=  {
            "transaction_b64": data , 
            "signature": signature
        }).content       

    def mine( self ): 
        return requests.get( "http://" + self.host + "/mine" ).content
    
    def ico(self, pk): 
        return requests.post( "http://" + self.host + "/ico" , data=  {
            "pk": pk
        }).content
    
    
    def add_data(self, data , signature , dataset ): 
        return requests.post( "http://" + self.host + "/add_valdata_stake" , data=  {
            "transaction_b64": data , 
            "signature": signature, 
            "dataset": dataset
        }).content
    
    def add_account(self, data , signature): 
        return requests.post( "http://" + self.host + "/new_account" , data=  {
            "transaction_b64": data , 
            "signature": signature
        }).content        
        
        
