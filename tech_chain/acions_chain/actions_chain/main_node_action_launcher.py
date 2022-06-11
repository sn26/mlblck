import argparse
import random

def main(): 
    try: 
        args = parse_args()
        script_main_function( args)
    except Exception as e: 
        print(e)
        print("ERROR: Error sending the request")


def script_main_function(args): 
    from library_chain.service_factory import MainChainService
    from library_client_chain.services import ClientServiceSender 
    from preprocessor.service import Preprocessor 
    from library_chain.dataset import DatasetPreprocessor
    from library_chain.api import BlockRequestsSender
    from library_chain.chain_factory import ChainFactory
    BlockRequestsSender.chain = ChainFactory.create_chain(2) #Le pasamos una chain que ya lleve añadido el nodo contra el que nos vamos a contectar para hacer las pruebas
    #Hacemos que el dataset preprocessor preprocese los datasets con el algoritmo que nos hemos creado para la chain
    DatasetPreprocessor.preprocessor = Preprocessor( ) 
    mainservice = MainChainService() #Inicializamos el nodo (Deberemos tener el admin file path puesto)
    mainservice.launchme( args.main_node_host , args.main_node_port) #Lanzamos el servidor
    return

    

#Function to get the entrance arguments from the client
def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-mnh", "--main-node-host", action='store', required=True,
                        help="Main Node Host. Required")
    parser.add_argument("-mnp", "--main-node-port", action='store', required=True,
                        help="Main Node Port. Required")
    return parser.parse_args( )

if __name__ == "__main__":
    main()
