from library_chain.tools import ChainUtils
from library_chain.transactions import TransactionFee
import time
from library_chain.models import HashManager

class Transaction:

    types = ["new_validator", "client"]

    def __init__(self):
        self.id = ChainUtils.gen_id()
        self.type = None #Solo permitimos sender + wallet o validador + pesos
        self.input = None
        self.output = None
        return

    #Solo tenemos dos opciones de transacciones 
    #TRANSACCIONES PARA AÑADIR PESOS: SENDER + WEIGHTS 
    #TRANSACCIONES PARA AÑADIR VALIDADORES: SENDER + VALIDATOR (DATASET + POS )
    @staticmethod
    def newTransaction(senderWallet, transaction , transaction_type ):
        if(transaction_type not in Transaction.types ): 
            return "ERROR: Transaction Type not found"
        fee = 0
        if( transaction_type == Transaction.types[0]):
            if ( senderWallet.toString( )["Balance"] < TransactionFee.fee): 
                return "ERROR: Not enough balance"
            fee = Transaction.fee
        return self.generateTransaction( senderWallet, transaction , transaction_type, fee)

    #SI LA TRANSACCION ES PARA AÑADIR PESOS, EN TRANSACTION CONTAREMOS CON LOS PESOS DEL MODELO, SINO, CONTAREMOS CON LOS DATASETS NECESARIOS
    @staticmethod
    def generateTransaction( senderWallet , transaction , transaction_type , fee): 
        transaction = Transaction( )
        transaction.type = transaction_type 
        transaction.output = {
            "fee": fee, 
            "sender": senderWallet, 
            "transaction": transaction
        }
        return transaction 

    #Function to sign a transaction with the validator
    @staticmethod
    def signTransaction( validatorWallet, transaction ): 
        transaction.input = {
            "timestamp": time.time(), 
            "from": validatorWallet.publicKey, 
            "signature": validatorWallet.sign( HashManager.get_hash(transaction.output ))
        }
       return 
    
    @staticmethod
    def verifyTransaction( transaction ): 
        return ChainUtils.verifySignature(
            transaction.input["from"],
            transaction.input["signature"],
            HashManager.get_hash(transaction.output)
        )