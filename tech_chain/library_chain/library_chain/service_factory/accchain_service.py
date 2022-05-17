from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from library_chain.api import ChainFactory
from librar_chain.wallets import wallet
import time 
import requests
from library_chain.transactions import TransactionPool
from library_chain.transaction import TransactionTypes

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument( 'pk' )
acc_chain = ChainFactory.create_chain(2)
wallet = None #Antes de iniciar el servicio, los datos internos de la wallet no estarán disponibles dentro del servicio, necesitaremos tenerlos dentro de nuestra wallet

acc_chain.create_genesis_block()
transactionPool = TransactionPool() #Lo definiremos dentro del init de la main chain
peers = set() #Address to other participating on the network

#Clase que implementa los servicios para el conteo de los usuarios (Wallets)
class AccChainService(): 

    

    #Añadimos una nueva transaccion (Lo tendremos que añadir a la nueva pool)
    #Cuando añadimos una nueva transacción, nos referimos a las que son de transferencia de dinero
    @app.route('/new_transaction', methods=['POST'])
    def add_transaction( self ): 
        args = parser.parse_args()
        for field in ["pk", "fee",  "ammount", "signature",  "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404
        args.append("timestamp") = time.time()
        args.append("TransactionType") = TransactionTypes.ADDTRANSACTION
        acc_chain.add_new_transaction( args)
        return "Success", 201 

    #Añadimos una nueva transaccion para añadir un nuevo validador a nuestra cadena 
    @app.route('/new_validator', methods=['POST'])
    def add_validator( self): 
        args = parser.parse_args( )
        for field in ["pk", "fee", "ammount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        args.append("timestamp") = time.time()
        args.append("TransactionType") = TransactionTypes.VALIDATOR
        acc_chain.add_new_transaction(args)
    
    #Añadimos un endpoint para añadir una nueva clave pública (acc) a nuestra cadena
    @app.route('/add_stake', methods=['POST'])
    def add_account( self ): 
        args = parser.parse_args( )
        for field in ["pk", "fee", "ammount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        args.append("timestamp") = time.time()
        args.append("TransactionType") = TransactionTypes.ADDSTAKE
        acc_chain.add_new_transaction(args)
    
    #Añadimos un endpoint para añadir una nueva clave pública (acc) a nuestra cadena
    @app.route('/add_valdata_stake', methods=['POST'])
    def add_account( self ): 
        args = parser.parse_args( )
        for field in ["pk", "fee", "ammount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        args.append("timestamp") = time.time()
        args.append("TransactionType") = TransactionTypes.ADDVALDATASTAKE
        acc_chain.add_new_transaction(args)



    #Añadimos un endpoint para añadir una nueva clave pública (acc) a nuestra cadena
    @app.route('/new_account', methods=['POST'])
    def add_account( self ): 
        args = parser.parse_args( )
        for field in ["pk", "fee", "ammount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        args.append("timestamp") = time.time()
        args.append("TransactionType") = TransactionTypes.ADDADDRESS
        acc_chain.add_new_transaction(args)

    #Sacamos toda la info de los bloques de la cadena
    @app.route('/chain', methods=['GET'])
    def get_chain(self): 
        chain_data = []
        for block in acc_chain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data),
                        "chain": chain_data,
                        "peers": list(peers)})
    
    
    #Endpoint para hacer que un validador nos firme un hash
    @app.route('/sign', methods=["GET"])
    def sign(self): 
        if ( args["hash"] == None ) return json.dumps( {
            "signature": "0"
        })
        #Si nuestro nodo es el validador de entre todos los nodos
        if acc_chain.get_validator( ) == wallet.public_key: 
            return json.dumps( {
                "signature": wallet.sign(args["hash"])
            })
        #Si no somos el validador, enviamos al resto de los nodos para que alguno nos lo firme
        for node in peers: 
           
            response["signature"] = str( requests.get('{}/sign'.format(node) , params= args  ).json()) 
            if response["signature"] != "0": 
                return json.dumps( response)
        return json.dumps( {
            "signature": "0"
        })

    #ENDPOINT PARA SACAR EL DATASET DE UN VALIDADOR
    @app.route('/dataset' , methods=["GET"])
    def dataset(self): 
        #Si nuestro nodo es el validador de entre todos los nodos
        if acc_chain.get_validator( ) == wallet.public_key: 
            return json.dumps( {
                "dataset": wallet.get_dataset()
            })
        #Si no somos el validador, enviamos al resto de los nodos para que alguno nos lo firme
        for node in peers: 
           
            response["dataset"] = str( requests.get('{}/dataset'.format(node)  ).json()) 
            if response["dataset"] != "0": 
                return json.dumps( response)
        return json.dumps( {
            "dataset": "0"
        })

    #Minado de las transacciones que no se hayan confirmado aún
    @app.route('/mine', methods['GET'])
    def mine(self):
        if len( acc_chain.transactionPool.transactions ) == 0: 
            return "No transactions to mine"
        result = acc_chain.mine() 
        if result == False: 
            return "ERROR: Invalid transactions"
        chain_length = len(acc_chain.chain) 
        self.consensus()
        if chain_length == len(acc_chain.chain):
            # announce the recently mined block to the network
            self.announce_new_block(acc_chain.last_block)
        return "Block #{} is mined.".format(acc_chain.last_block.index)

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
            global acc_chain
            global peers
            # update chain and the peers
            chain_dump = response.json()['chain']
            acc_chain = create_chain_from_dump(chain_dump)
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
        if ( acc_chain.add_block(block ) == False): 
            return "The block was discarded by the node", 400
        return "Block added to the chain", 201

    @app.route('/pending_transactions', methods=["GET"])
    def get_pending_transactions(): 
        return json.dumps(acc_chain.transactionPool.transactions)
        

    #Function to create a new wallet
    @app.route('/wallet', methods=["POST"])
    def create_wallet(self): 
        wallet = wallet( args["secret"]  )
        return wallet 
    
    def create_chain_from_dump(self , chain_dump): 
        generated_chain = ChainFactory.create_chain(2)
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
        global acc_chain
        longest_chain = None 
        current_len = len(acc_chain.chain)
        for node in peers:
            response = requests.get('{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            if length > current_len and acc_chain.check_chain_validity(chain):
                current_len = length
                longest_chain = chain

        if longest_chain != None:
            acc_chain = longest_chain
            return True

        return False
    
    def announce_new_block(self , block ): 
        for peer in peers:
            url = "{}add_block".format(peer)
            headers = {'Content-Type': "application/json"}
            requests.post(url,
                        data=json.dumps(block.__dict__, sort_keys=True),
                        headers=headers)

