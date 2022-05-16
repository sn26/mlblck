from library_chain.transactions import Transaction

class TransactionPool: 

    def __init__(self): 
        self.transactions = []
        return 

    def get_pending_transactions(self): 
        return self.transactions
    
    def add_transaction(self, transaction ): 
        self.transactions.append(transaction )
        return 

    def validTransactions(self  ): 
        for i in range( 0, len(self.transactions )): 
            if( Transaction.verifyTransaction( self.transactions[i]) == 0 ) :
                return 0, "ERROR: Some transactions in transaction pool are not verified" 
        return 1, "Ok"