import requests 

#Class to send rquest to the cnn server 
class ClientRequestSender():
    
    def __init__(self , host):
        self.host = host
        return
    
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
    
    
    def add_data(self, data , signature): 
        return requests.post( "http://" + self.host + "/add_valdata_stake" , data=  {
            "transaction_b64": data , 
            "signature": signature
        }).content
    
    def add_account(self, data , signature): 
        return requests.post( "http://" + self.host + "/new_account" , data=  {
            "transaction_b64": data , 
            "signature": signature
        }).content        
        
        
