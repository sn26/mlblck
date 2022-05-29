
#Proof of stake 
#Each validator has to add a dataset to being a validator
class MiningFeature: 

    #Passing the wallet name and password
    def __init__(self, accounts): 
        #self.addresses = []
        self.balance = {}
        self.validators = [] 
        self.accounts = accounts 
        self.datasets = {}
        self.rest_addresses = {}
        return


    def update( self ,transaction  ): 
        print("Entramos a actualizar el validador")
        print("VALIDACION")
        if ( transaction["amount"] >= 1 and transaction["to"] == "0"  and transaction["validator_endpoint_address"] != None and transaction["dataset"] != None): 
            if transaction["pk"] not in self.accounts.addresses: 
                print("ERROR: THERE IS NOT AN ACCOUNT WITH THE GIVEN PK ")
                return False 
            if self.accounts.balance[transaction["pk"]] < transaction["amount"]:
                print("ESTAMOS ENTRANDO EN EL BALANCE Y HEMOS DADO FALSE!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(self.accounts.balance[transaction["pk"]])
                print(transaction["amount"])
                return False
            print("LA VALIDACION HA SIDO CORRECTAAAAAAAAAAAAAAAAAAAAAAA")
            self.validators.append( transaction["pk"])
            self.rest_address[transaction["pk"]] = transaction["validator_endpoint_address"]
            self.datasets[transaction["pk"]] = transaction["output"]["dataset"] #Añadimos el dataset del validador 
            self.accounts.addresses.balance[transaction["pk"]] = self.accounts.addresses.balance[transaction["pk"]] - transaction["amount"] #Retiramos de lo que tenemos en accounts
            return True
        return False

    def check_validators_addr(self,  address ): 
        if address not in self.accounts.addresses :
            print("ERROR: THERE IS NOT AN ACCOUNT WITH THE GIVEN PK")
            return False 
        if address not in self.validators: 
            return False
        return True

    def initialize(self, address):
        if self.check_validators_addr( address )== False: 
            return
        if (self.balance[address] == None):
            self.balance[address] = 0
            #self.validators.append( address)
        return

    def addStake(self, from_tr, amount): 
        if self.check_validators_addr(from_tr) == False: 
            return
        self.initialize(from_tr)
        self.balance[from_tr] = self.balance[from_tr ] + amount
        return 
    
    def addValidationData(self , from_tr ,datasets): 
        if self.check_validators_addr(address) == False: 
            return 
        self.initialize(from_tr )
        self.datasets[from_tr] = self.datasets[from_tr] + datasets
        return 
  
    def getStake(self, address):
        if self.check_validator_addr(address) == False: 
            return 
        self.initialize(address)
        return self.balance[address] 

    def getMax(self):
        balanceplusdata = -1
        leader = None
        try: 
            for i in range( 0 , len(self.validators )): 
                if (self.balance[self.validators[i]]*0.4 + len(self.datasets[self.validators[i]])*0.6> balanceplusdata):
                    leader = self.validators[i]                
                    balance= self.balance[self.validators[i]]*0.4 + len(self.datasets[self.validators[i]])*0.6
            #Returns the leader which is going to be used for validate 
            return leader
        except Exception as e: 
            return None

    def getNonce(self ): 
        val = self.getMax()
        return self.balance[val]*0.4 + len(self.datasets[val])*0.6

    '''
    def update(self, transaction): 
        self.addStake(transaction["pk"] , transaction["amount"] )
        return 
    '''