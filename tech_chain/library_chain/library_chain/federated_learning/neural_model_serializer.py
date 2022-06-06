from keras.models import model_from_json
import base64 
import gzip 
import json
import ast 
import numpy
from numpy import array
from numpy import float32
import ast

class NeuralModelSerializer: 

    @staticmethod
    def decode_from_model_weights(model):
        
        print("ESTAMOS PASANDO A REALIZAR LA DECODIFICACION ")
        args = base64.decodebytes( model.replace("\"", "").replace("\\n" , "\n").encode("utf-8")) 
        print(args)
        print("AHORA PASAMOS A DESCOMPRIMIRLO")
        args = gzip.decompress( args ).decode("utf-8") 
        print(args)
        print("AHORA ESTAMOS PASANDO A SACAR LO QUE CONTIENE EL ULT BASE  64")
        args = base64.decodebytes( bytes ( args.replace("\"", "").replace("\\n" , "\n").replace("'" , "\"")  , "utf-8")  ).decode("utf-8")
        #Una vez que tenemos los args, nos generaremos el json y luego haremos una lista con los numpy arrays concatenados
        print("EL RESULTADO QUE TENIAMOS ANTES DE PASAR ES ")
        print(args.replace("\\\\", "\\").replace("," , ",\n").replace("'" , "\"").replace("\"{", "{").replace("}\"", "}"))
        res = json.loads(args.replace("\\\\", "\\").replace("," , ",\n").replace("'" , "\"").replace("\"{", "{").replace("}\"", "}")) 
        wghts = []
        counter = 0
        keys_lst=  list( res.keys() ) 
        for i in range(0 ,len(res.keys())): 
            if counter >= len(res.keys()): 
                return wghts
            wghts.append(numpy.frombuffer( base64.decodebytes( bytes( res[keys_lst[counter]] , "utf-8") ), dtype=numpy.single))
            print("LO QUE ESTAMOS SACANDO DE LA TUPLA ES") 
            print(base64.decodebytes( bytes( res[keys_lst[counter + 1] ] , "utf-8") ).decode("utf-8"))
            print(type( ast.literal_eval(ast.literal_eval(base64.decodebytes( bytes( res[keys_lst[counter + 1] ] , "utf-8") ).decode("utf-8"))) ))
            wghts[-1] = wghts[-1].reshape( ast.literal_eval(ast.literal_eval(base64.decodebytes( bytes( res[keys_lst[counter + 1] ] , "utf-8") ).decode("utf-8"))) )
            counter = counter + 2 
        print("ESTAMOS SALIENDO A SACAR EL NUMPY NUEVAMENTE")
        print(len(wghts))
        return wghts        

    @staticmethod
    def decode_from_model_arch( model): 
        print("ESTAMOS PASANDO A REALIZAR LA DECODIFICACION ")
        args = base64.decodebytes( model.replace("\"", "").replace("\\n" , "\n").encode("utf-8")) 
        print(args)
        print("AHORA PASAMOS A DESCOMPRIMIRLO")
        args = gzip.decompress( args ).decode("utf-8") 
        print(args)
        print("AHORA ESTAMOS PASANDO A SACAR LO QUE CONTIENE EL ULT BASE  64")
        args = base64.decodebytes( bytes ( args.replace("\"", "").replace("\\n" , "\n").replace("'" , "\"")  , "utf-8")  ).decode("utf-8")
        print(args)
        print("DEVOLVEMOS EL RESULTADO DE VUELTA")
        print("EL RESULTADO ES ")
        print(json.loads(args.replace("\\", "").replace("," , ",\n").replace("'" , "\"").replace("\"{", "{").replace("}\"", "}")))
        return json.loads(args.replace("\\", "").replace("," , ",\n").replace("'" , "\"").replace("\"{", "{").replace("}\"", "}"))
        

    #Metodo que nos permite serializar un modelo de red neuronal
    @staticmethod 
    def serialize( block): 
        #Cuando vayamos a serializar el modelo del bloque, 
        #lo primero que tendremos que hacer es decodificar el b64 que tenemos de entrada   
        model = model_from_json(json.dumps( NeuralModelSerializer.decode_from_model_arch(block["model"] )))
        model.set_weights(NeuralModelSerializer.decode_from_model_weights(block["model_weights"]))
        return model
