from library_chain.utils import ChainUtils
from library_chain.transactions import TransactionFee
import time
from library_chain.models import HashManager
from library_chain.transactions import TransactionTypes

class Transaction:

    #Nuestras transacciones serán diferentes para cada bloque, cada transaccion se almacena en un diccionnario, por lo que nos da igual
    #Aqui solo firmaremos transacciones y les haremos un check
    @staticmethod
    def add_id_to_transaction(transaction ): 
        transaction["id"] = ChainUtils.gen_id()
        return transaction

    


    ''' 
    #Funcion que me verifica una transaccion
    @staticmethod
    def verifyTransaction( transaction ): 
        #Para sacar el hash de la transaccion, borraremos el hash de la transaccion y lo generaremos a mano
        try: 
            del transaction["digest"]
            del transaction["timestamp"]
        except Exception as e: 
            passs
        return ChainUtils.verifySignature(
            transaction["pk"],
            transaction["signature"],
            HashManager.get_hash(transaction)
        )
    
    #Function to sign a transaction with the validator
    @staticmethod
    def signTransaction( validatorWallet, transaction ): 
        transaction = {
            "timestamp": time.time(), 
            "from": validatorWallet.publicKey, 
            "signature": validatorWallet.sign( HashManager.get_hash(transaction.output ))
        }
       return 
    
    #Solo tenemos dos opciones de transacciones 
    #TRANSACCIONES PARA AÑADIR PESOS: SENDER + WEIGHTS 
    #TRANSACCIONES PARA AÑADIR VALIDADORES: SENDER + VALIDATOR (DATASET + POS )
    @staticmethod
    def newTransaction(transaction , transaction_type ):
        if(transaction_type not in Transaction.TYPES ): 
            return "ERROR: Transaction Type not found"
        fee = 0
        if( transaction_type == Transaction.TYPES[0]):
            if ( senderWallet.toString( )["Balance"] < TransactionFee.fee): 
                return "ERROR: Not enough balance"
            fee = Transaction.fee
        return self.generateTransaction(  transaction , transaction_type, fee)

    #SI LA TRANSACCION ES PARA AÑADIR PESOS, EN TRANSACTION CONTAREMOS CON LOS PESOS DEL MODELO, SINO, CONTAREMOS CON LOS DATASETS NECESARIOS
    @staticmethod
    def generateTransaction( transaction , transaction_type , fee): 
        transaction = Transaction( )
        transaction.type = transaction_type 
        transaction.output = {
            "fee": fee, 
            "transaction": transaction
        }
        return transaction 
    ''' 
    