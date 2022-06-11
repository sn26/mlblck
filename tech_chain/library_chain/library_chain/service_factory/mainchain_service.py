from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from library_chain.chain_factory import ChainFactory, ChainSerializer
from library_chain.wallets import Wallet
import time 
import requests
from library_chain.service_factory import ServiceTools
from library_chain.transactions import TransactionTypes
import os 
import json 
import base64 
import gzip 
from library_chain.models import BlockSerializer 
from library_chain.models import HashManager

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
#PK -> CLAVE PUBLICA DEL AUTHOR DE UNA TRANSACCION 
parser.add_argument('transaction_b64')
parser.add_argument('rest_federated_blocks')
parser.add_argument('signature')
parser.add_argument('block_hash')
parser.add_argument('node_address')
parser.add_argument('X') #La data de la que queremos sacar la prediccion

class MainChainService():


    main_chain = ChainFactory.create_chain(0)
    peers = set()

    @app.route('/newest_neural_prediction', methods=['GET'])
    def get_neural_block_prediction():
        args = parser.parse_args() 
        return main_chain.get_response_from_last_block(args["X"] )
    
    @app.route('/neural_prediction_from_one_block', methods=['GET'])
    def get_neural_block_prediction_by_hash():
        args = parser.parse_args()
        return main_chain.get_response_from_hash_block(args['hash'], args['X'])

    #Añadimos una nueva transaccion (Lo tendremos que añadir a la nueva pool)
    @app.route('/new_federated_lerning_model', methods=['POST'])
    def add_transaction(  ): 
        args = parser.parse_args( )
        if args["rest_federated_blocks"] == None: 
            return "Invalid Transaction data", 404 
        rfb = args["rest_federated_blocks"]    
        signature = ServiceTools.decode_signature( args["signature"])
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "rest_federated_blocks", "signature", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        return {"Success":201 ,  "Result":  MainChainService.main_chain.add_new_transaction({
            "pk": args["pk"], 
            "rest_federated_blocks": rfb , 
            "signature": args["signature"],  
            "digest": args["digest"], 
            "timestamp": time.time()
        })}
    
    #Sacamos toda la info de los bloques de la cadena
    @app.route('/chain', methods=['GET'])
    def get_chain(): 
        chain_data = []
        for block in MainChainService.main_chain.chain:
            chain_data.append(block.to_string())
        return json.dumps({"length": len(chain_data),
                        "chain": chain_data,
                        "peers": list( MainChainService.peers) })

    #Minado de las transacciones que no se hayan confirmado aún
    @app.route('/mine', methods=['GET'])
    def mine():
        if len( MainChainService.main_chain.unconfirmed_transactions ) == 0: 
            return {"Result": "No Transactions to mine."}
        result = MainChainService.main_chain.mine() 
        if result == False: 
            MainChainService.main_chain.unconfirmed_transactions.clear() #Limpiamos el conjunto de transacciones con las que contaba la chain
            return {"Result": "ERROR: Invalid transactions" }
        chain_length = len(MainChainService.main_chain.chain) 
        #return {"Result": "Evitamos el consenso"}
        print(" Estamos entrando para realizar el consenso con todas las peers ")
        if( MainChainService.consensus() == True):
            #MainChainService.main_chain.unconfirmed_transactions.clear() #Limpiamos las transacciones una vez hemos minado el bloque
            return {"Result": "Consesus from another node. No block mined but chain changed", "Chain": MainChainService.get_chain() } 
        if chain_length == len(MainChainService.main_chain.chain):
            # announce the recently mined block to the network
            MainChainService.announce_new_block(MainChainService.main_chain.last_block)
        MainChainService.main_chain.unconfirmed_transactions.clear() #Limpiamos las transacciones una vez hemos minado el bloque
        return {"Result": "Block #{} is mined.".format(MainChainService.main_chain.last_block.index) }
    
    #Endpoint to add peers
    @app.route('/register_node', methods=['POST']) 
    def register_peer():
        node_address = request.get_json()["node_address"]
        if node_address == None:  
            return "ERROR: Invalid data" , 400 
        MainChainService.peers.add( request.host_url ) #Nos concatenamos a nosotros mismos 
        MainChainService.peers.add( node_address )
        print("NUESTRO ROOT CHAIN TIENE ")
        print(MainChainService.peers)
        return MainChainService.get_chain()
    
    @app.route('/register_with' , methods= ['POST'])
    def register_with_existing_node(): 
        node_address = request.get_json()["node_address"]
        if node_address == None:
            return "Error: Invalid data", 400
        data = {"node_address": request.host_url}
        headers = {'Content-Type': "application/json"}
        # Make a request to register with remote node and obtain information
        response = requests.post(node_address + "/register_node",
                                data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            # update chain and the peers
            chain_dump = response.json()['chain']
            #Le pasamos la wallet que ya teníamos creada para conseguir persistirla
            MainChainService.main_chain = MainChainService.create_chain_from_dump(chain_dump )
            #Nos añadimos a la chain
            for i in range( 0 , len( response.json()['peers'])):
                MainChainService.peers.add(response.json()['peers'][i]) #Concatenamos las peers en nuestra lista
            return "Registration successful", 200
        else:
            # if something goes wrong, pass it on to the API response
            return response.content, response.status_code
        
 
    @app.route('/add_block', methods=["POST"])
    def verify_and_add_block(): 
        block_data = request.get_json()
        block = BlockSerializer.serialize( block_data)
        if ( MainChainService.main_chain.add_block(block ) == False): 
            return "The block was discarded by the node", 400
        return "Block added to the chain", 201
    

    @app.route('/pending_transactions', methods=["GET"])
    def get_pending_transactions(): 
        res = []
        for transaction in MainChainService.main_chain.unconfirmed_transactions : 
            res.append( HashManager.delete_unnecesary_params_from_transaction( transaction ))
        return {"Success":201, "Result": res }
        
        
        
    def create_chain_from_dump(chain_dump): 
        MainChainService.main_chain = ChainSerializer.serialize_main_chain( chain_dump) #Serializamos la chain de los usuarios, para que coincida con lo que tenemos interno
        return MainChainService.main_chain

    
    def consensus( ): 
        longest_chain = None 
        current_len = len(MainChainService.main_chain.chain)
        for node in MainChainService.peers:
            print("Nuestros nodos son ")
            print( node)
            response = requests.get('{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            if length > current_len and MainChainService.main_chain.check_chain_validity(chain) == True:
                current_len = length
                longest_chain = chain
        print(" HEMOS SACADO EL CONSENSO")
        if longest_chain != None:
            print("ESTAMOS CAMBIANDO NUESTRA CHAIN!!!!!!!!!!!!!!!")
            #MainChainService.main_chain.wallet_setup( )
            #MainChainService.set_new_validator() #Seteamos nuevamente nuestra wallet como validadora
            MainChainService.main_chain = ChainSerializer.serialize_main_chain( longest_chain ) #Serializamos la chain de los usuarios, para que coincida con lo que tenemos interno
            return True
        return False
        
    
    def announce_new_block( block ): 
        for peer in list( MainChainService.peers):
            url = "{}/add_block".format(peer)
            headers = {'Content-Type': "application/json"}
            requests.post(url,
                        data=json.dumps(block.to_string(), sort_keys=True),
                        headers=headers)

    def launchme( self , host , port ): 
        #api.add_resource(MainChainService , '/UserChain')
        #MainChainService.main_chain.wallet_setup( )
        MainChainService.main_chain.create_genesis_block() #Le pasamos la wallet para firmar el bloque
        app.run( host= host , port=port, debug =False )
       



if __name__ == "__main__":
    
    print("ESTAMOS LANZANDO EL MAIN")    

