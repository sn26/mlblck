import argparse

def main(): 
    try: 
        args = parse_args()
        script_main_function( args)
    except Exception as e: 
        print(e)
        print("ERROR: Error sending the request")


def script_main_function(args): 
    from library_chain.service_factory import AccChainService
    from library_chain.wallets import Wallet
    from library_client_chain.services import ClientServiceSender 

    accservice = AccChainService() #Inicializamos el nodo (Deberemos tener el admin file path puesto)
    accservice.acc_chain.set_chain_wallet(args.node_wallet_file) #Seteamos la wallet que tendrá la chain
    #Nor cargamos un cliente con el nodo al que nos vamos a registrar 
    csr = ClientServiceSender( str( args.host_node_register_with) + ":" + str(args.port_node_register_with) , accservice.acc_chain.wallet)
    #Una vez tenemos la wallet, se la pasaremos al nodo al que nos vamos a registrar en forma de transaccion
    csr.mine() #Intentamos borrar cualquier transaccion dentro del nodo, para asegurar que el conjunto de transacciones que vamos a meter no va a dar fallo
    csr.add_account( ) #Añadimos la wallet que acabamos de crear, e intentamos hacer un ico hacia nuestra wallet
    csr.ico( )
    csr.mine()
    #Una vez hemos añadido la cuenta, inicializaremos el nodo, preparado para que el usuario pueda registrarse al nodo concreto
    #accservice.set_user_chain("http://" + args.host_node_register_with + ":" + args.port_node_register_with + "/")
    print("NODE SERVER IS GOING TO BE ENABLED: \n USE REGISTER WITH TO ADD THIS NODE TO THE CHAIN!!")
    accservice.launchme( args.main_node_host , args.main_node_port) #Lanzamos el servidor
    
    return

    

#Function to get the entrance arguments from the client
def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-mnh", "--main-node-host", action='store', required=True,
                        help="Main Node Host. Required")
    parser.add_argument("-mnp", "--main-node-port", action='store', required=True,
                        help="Main Node Port. Required")
    parser.add_argument("-nwf" , "--node-wallet-file", action='store', required=True , 
            help="User Node Wallet File. Required")
    #Nodo que usaremos para registrarnos como un nuevo nodo
    parser.add_argument("-hnrw","--host-node-register-with", action='store', 
                    required=True, help="Node from with this node will be registered. Required")
    parser.add_argument("-pnrw","--port-node-register-with", action='store', 
                    required=True, help="Node from with this node will be registered. Required")

    
    return parser.parse_args( )

if __name__ == "__main__":
    main()
