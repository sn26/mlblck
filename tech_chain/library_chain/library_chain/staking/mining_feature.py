
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
    
    def get_len_from_dataset(self, dataset): 
        if type(dataset ) == list: #Comprobamos si no lo tenemos inicializado con un dataset
            print("HEMOS ENTRADO PORQUE NUESTRO TIPO ES UNA LISTA")
            return len(dataset)
        print("NO HEMOS ENTRADO ")
        print("EL TIPO ES ")
        print(type(dataset))
        data_len = 0 
        for key in dataset.keys():
            data_len = data_len + len( dataset[key]) 
        return data_len

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
            self.rest_addresses[transaction["pk"]] = transaction["validator_endpoint_address"]
            self.datasets[transaction["pk"]] = transaction["dataset"] #Añadimos el dataset del validador 
            self.balance[transaction["pk"]] =  transaction["amount"] #Añadimos el balance
            self.accounts.balance[transaction["pk"]] = self.accounts.balance[transaction["pk"]] - transaction["amount"] #Retiramos de lo que tenemos en accounts
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
        if ( address not in self.balance.keys()):
            self.balance[address] = 0
            self.datasets[address] = []
            self.validators.append(address)
            self.rest_addresses[address] = self.rest_addresses[self.rest_addresses.keys()[0]]
            #self.validators.append( address)
        return

    def addStake(self, from_tr, amount): 
        if self.check_validators_addr(from_tr) == False: 
            return
        self.initialize(from_tr)
        self.balance[from_tr] = self.balance[from_tr ] + amount
        return 
    
    def addValidationData(self , from_tr ,datasets): 
        if self.check_validators_addr(from_tr) == False: 
            print("ERROR: THERE IS NOT A USER TO ADD VAL DATA")
            return 
        self.initialize(from_tr )
        if len(self.datasets[from_tr ]) == 0: 
            self.datasets[from_tr] = datasets
            return
        else: 
            try:
                for key in self.datasets[from_tr].keys( ):
                    self.datasets[from_tr][key].extend( datasets[key])
            except Exception as e: 
                print("ERROR: Keys dont' match!")
                return
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
                if (int(self.balance[self.validators[i]])*0.4 +  int(self.get_len_from_dataset(self.datasets[self.validators[i]]))*0.6> balanceplusdata):
                    leader = self.validators[i]                
                    balance= int(self.balance[self.validators[i]])*0.4 + len(self.datasets[self.validators[i]])*0.6
            #Returns the leader which is going to be used for validate 
            return leader
        except Exception as e: 
            print("HEMOS LANZADO UNA EXCEPCION AL SACAR EL LEADER")
            return None

    def getNonce(self ): 
        val = self.getMax()
        return self.balance[val]*0.4 + len(self.datasets[val])*0.6

    '''
    def update(self, transaction): 
        self.addStake(transaction["pk"] , transaction["amount"] )
        return 
    '''