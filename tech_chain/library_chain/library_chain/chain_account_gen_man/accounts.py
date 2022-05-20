

class Accounts: 

    def __init__(self ): 
        self.addresses = []
        self.balance = {}
        return 

    #Function to add a new address into or Main Acc
    def add_address(self, address): 
        try: 
            if ( self.balance[address] != None): 
                return "Address Already Exists at node!"  
        except Exception as e: 
            self.balance[address] = 0
            self.addresses.append(address)
        return self.addresses

    #Not currently working!  
    #def transfer( from , to, amount ): 
    def transfer(self, from_tr, to, amount): 
        if amount > self.getBalance(from_tr): 
            return "ERROR: Not enough money at wallet"
        self.add_address(from_tr)
        self.add_address(to) 
        self.increment(to, amount)
        self.decrement(from_tr, amount)
        return

    def increment(self, to, amount):
        self.balance[to] = amount + self.balance[to] 

    def decrement( self, from_tr, amount):
        self.balance[from_tr] = self.balance[from_tr] - amount 

    def getBalance(self, address):
        self.add_address(address) 
        return self.balance[address]
    
   
