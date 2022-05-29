import base64
import gzip 
import json

class ServiceTools: 

    #Function to decode base64 transaction
    @staticmethod
    def decode_transaction(transaction ):
        args = base64.decodebytes( transaction.replace("\"", "").replace("\\n" , "\n").encode("utf-8"))
        args =  json.loads( gzip.decompress( args ).decode("utf-8") )
        args = base64.decodebytes( bytes ( args , "utf-8")  ).decode("utf-8")
        res = json.loads(args.replace("\"", "").replace("\\n" , "\n").replace("'" , "\"") )
        return res 


    #Funcion que decodifica las firmas de las transacciones
    @staticmethod
    def decode_signature( signature): 
        return base64.decodebytes( signature.replace("\"", "").replace("\\n" , "\n").encode("utf-8"))
    