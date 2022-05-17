
#Proof of stake 
#Each validator has to add a dataset to being a validator
class MiningFeature: 

    #Passing the wallet name and password
    def __init__(self): 
        self.addresses = []
        self.balance = {}
        self.validators = [] 
        self.datasets = {}
        return

    def update( self ,transaction): 
        if ( transaction["amount"] == 1 and transaction["to"] == "0"  and trasaction.transaction["dataset"] != None): 
            self.validators.append( transaction["from"])
            self.datasets[transaction["from"]] = transaction["output"]["dataset"] #Añadimos el dataset del validador 
            return True
        return False

    def check_validators_addr(self,  address ): 
        if address not in self.validators: 
            return False
        return True

    def initialize(self, address) {
        if self.check_validators_addr( address )== False: 
            return
        if (self.balance[address] == None):
            self.balance[address] = 0
            self.addresses.append( address)
        return

    def addStake(self, from, amount): 
        if self.check_validators_addr(from) == False: 
            return
        self.initialize(from)
        self.balance[from] = self.balance[from ] + amount
        return 
    
    def addValidationData(self , from ,datasets): 
        if self.check_validators_addr(address) == False: 
            return 
        self.initialize(from )
        self.datasets[from] = self.datasets[from] + datasets
        return 
  
    def getStake(self, address):
        if self.check_validator_addr(address) == False: 
            return 
        self.initialize(address)
        return self.balance[address] 

    def getMax(self, addresses):
        balanceplusdata = -1
        leader = undefined
        for i in range( 0 , len(addresses )): 
            if (self.balance[addresses[i]]*0.4 + len(self.datasets[addresses[i]])*0.6> balanceplusdata):
                leader = address                
                balance= self.balance[addresses[i]]*0.4 + len(self.datasets[addresses[i]])*0.6
        #Returns the leader which is going to be used for validate 
        return leader

    def update(self, transaction): 
        self.addStake(transaction.input.from , transaction.output.amount )
        return 