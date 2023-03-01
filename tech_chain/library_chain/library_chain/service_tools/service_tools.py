import base64
import gzip 
import json

class ServiceTools: 

    #Function to decode base64 transaction
    @staticmethod
    def decode_transaction(transaction ):
        args = base64.decodebytes( transaction.replace("\"", "").replace("\\n" , "\n").encode("utf-8"))
        print("LO QUE TENEMOS DESPUES DE LA PRIMERA DECODIFICACION ES ")
        print(args)
        args =  json.loads( gzip.decompress( args ).decode("utf-8") )
        print("PASAMOS EL JSON Y NOS DA ")
        print(args)
        args = base64.decodebytes( bytes ( args , "utf-8")  ).decode("utf-8")
        print("PASAMOS EL B64 Y NOS DA ")
        print(args.replace("\"", "").replace("\\n" , "\n").replace("'" , "\"") )
        res = json.loads(args.replace("\"", "").replace("\\n" , "\n").replace("'" , "\"") )
        return res 


    #Funcion que decodifica las firmas de las transacciones
    @staticmethod
    def decode_signature( signature): 
        return base64.decodebytes( signature.replace("\"", "").replace("\\n" , "\n").encode("utf-8"))
    