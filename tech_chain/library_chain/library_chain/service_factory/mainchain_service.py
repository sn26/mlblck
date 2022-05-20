from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from library_chain.chain_factory import ChainFactory
from library_chain.wallets import Wallet
import time 
import requests
from library_chain.transactions import TransactionTypes
import os 
import json 
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
#PK -> CLAVE PUBLICA DEL AUTHOR DE UNA TRANSACCION 
parser.add_argument('hash', 'rest' , 'pk' )
main_chain = ChainFactory.create_chain(0)
#No necesitamos cargar ningun dataset, dado que nos vendrá por parte del usuario validador
main_chain.preprocessor = None #Necesitareemos cargar un preprocesado de los datos, que nos vendrá por parte del usuario
wallet = Wallet("ADM00")
main_chain.create_genesis_block(wallet)
peers = set() #Address to other participating on the network

class MainChainService():

    @app.route('/newest_neural_prediction', methods=['GET'])
    def get_neural_block_prediction(self):
        args = parser.parse_args() 
        return main_chain.get_response_from_last_block(args["X"] )
    
    @app.route('/neural_prediction_from_one_block', methods=['GET'])
    def get_neural_block_prediction_by_hash(self):
        args = parser.parse_args()
        return main_chain.get_response_from_hash_block(args['hash'], args['X'])

    #Añadimos una nueva transaccion (Lo tendremos que añadir a la nueva pool)
    @app.route('/new_transaction', methods=['POST'])
    def add_transaction( self ): 
        args = parser.parse_args()
        for field in ["hash", "rest", "author"]: 
            if field not in args: 
                return "Invalid Transaction data", 404
        args["timestamp"]= time.time()
        main_chain.add_new_transaction( args)
        return "Success", 201 
    
    #Sacamos toda la info de los bloques de la cadena
    @app.route('/chain', methods=['GET'])
    def get_chain(self): 
        chain_data = []
        for block in main_chain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data),
                        "chain": chain_data,
                        "peers": list(peers)})

    #Minado de las transacciones que no se hayan confirmado aún
    @app.route('/mine', methods=['GET'])
    def mine(self):
        if len( main_chain.transactionPool.transactions ) == 0: 
            return "No transactions to mine"
        result = main_chain.mine() 
        if result == False: 
            return "ERROR: Invalid transactions"
        chain_length = len(main_chain.chain) 
        self.consensus()
        if chain_length == len(main_chain.chain):
            # announce the recently mined block to the network
            self.announce_new_block(main_chain.last_block)
        
        return "Block #{} is mined.".format(main_chain.last_block.index)
    
    #Endpoint to add peers
    @app.route('/register_node', methods=['POST']) 
    def register_peer(self ):
        node_address = request.get_json()["node_address"]
        if not node_address: 
            return "ERROR: Invalid data" 
        peers.add( node_address )
        return self.get_chain()
    
    @app.route('/register_with' , methods= ['POST'])
    def register_with_existing_node(self ): 
        node_address = request.get_json()["node_address"]
        if not node_address:
            return "Invalid data", 400
        data = {"node_address": request.host_url}
        headers = {'Content-Type': "application/json"}
        # Make a request to register with remote node and obtain information
        response = requests.post(node_address + "/register_node",
                                data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            global main_chain
            global peers
            # update chain and the peers
            chain_dump = response.json()['chain']
            main_chain = create_chain_from_dump(chain_dump)
            peers.update(response.json()['peers'])
            return "Registration successful", 200
        else:
            # if something goes wrong, pass it on to the API response
            return response.content, response.status_code
        
    @app.route('/add_block', methods=["POST"])
    def verify_and_add_block(): 
        block_data = request.get_json()
        block = Block(block_data["index"],
                    block_data["transactions"],
                    block_data["timestamp"],
                    block_data["previous_hash"],
                    block_data["nonce"],
                    block_data["pk"])
        if ( main_chain.add_block(block ) == False): 
            return "The block was discarded by the node", 400
        return "Block added to the chain", 201

    @app.route('/pending_transactions', methods=["GET"])
    def get_pending_transactions(): 
        return json.dumps(main_chain.transactionPool.transactions)
        
        
    def create_chain_from_dump(self , chain_dump): 
        generated_chain = ChainFactory.create_chain(0)
        #Cargamos el dataset y el que se encargará de preprocesar los datos en la chain
        generated_chain.dataset = DataLoader.load_dataset()
        generated_chain.preprocessor = Preprocessor()
        generated_chain.create_genesis_block()
        for idx, block_data in enumerate(chain_dump):
            if idx == 0:
                continue  # skip genesis block
            block = Block(block_data["index"],
                        block_data["transactions"],
                        block_data["timestamp"],
                        block_data["previous_hash"],
                        block_data["nonce"])
           
            added = generated_blockchain.add_block(block)
            if not added:
                raise Exception("ERROR: Chain Security Fail")
        return generated_blockchain    

    
    def consensus(self ): 
        global main_chain
        longest_chain = None 
        current_len = len(main_chain.chain)
        for node in peers:
            response = requests.get('{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            if length > current_len and main_chain.check_chain_validity(chain):
                current_len = length
                longest_chain = chain

        if longest_chain != None:
            main_chain = longest_chain
            return True

        return False
    
    def announce_new_block(self , block ): 
        for peer in peers:
            url = "{}add_block".format(peer)
            headers = {'Content-Type': "application/json"}
            requests.post(url,
                        data=json.dumps(block.__dict__, sort_keys=True),
                        headers=headers)

