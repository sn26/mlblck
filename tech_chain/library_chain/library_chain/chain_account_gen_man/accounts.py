

class Accounts: 

    def __init__(self ): 
        self.addresses = []
        self.balance = {}
        return 

    #Function to add a new address into or Main Acc
    def add_address(self, address): 
        if (self.balance[address] == None):
            self.balance[address] = 0
            self.addresses.append(address)
        return 

    #Not currently working!  
    #def transfer( from , to, amount ): 
    def transfer(self, from, to, amount) 
        self.add_address(from)
        self.add_address(to) 
        self.increment(to, amount)
        self.decrement(from, amount)
        return

    def increment(self, to, amount):
        self.balance[to] = amount + self.balance[to] 

    def decrement( self, from, amount):
        self.balance[from] = self.balance[from] - amount 

    def getBalance(self, address):
        self.add_address(address) 
        return self.balance[address]
    
   
