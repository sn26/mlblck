import argparse

#


def main(): 
    try: 
        args = parse_args()
        script_main_function( args)
    except Exception as e: 
        print(e)
        print("ERROR: Error sending the request")

def script_main_function(args): 
    from library_chain.service_factory import AccChainService
    accservice = AccChainService() #Inicializamos el nodo
    accservice.acc_chain.set_chain_wallet(  args.adm_wallet_path  ) #Fijamos la wallet de lo que sería nuestro adm
    #accservice.set_user_chain("http://" + args.main_node_host + ":" + args.main_node_port + "/")
    accservice.launchme(args.main_node_host , args.main_node_port )
    return "NODE INITIALIZED"
    

#Function to get the entrance arguments from the client
def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-mnh", "--main-node-host", action='store', required=True,
                        help="Main Node Host. Required")
    parser.add_argument("-mnp", "--main-node-port", action='store', required=True,
                        help="Main Node Port. Required")
    parser.add_argument("-awp", "--adm-wallet-path", action='store', required=True,
                        help="Adm Wallet Path. Required")
    return parser.parse_args( )

if __name__ == "__main__":
    main()
