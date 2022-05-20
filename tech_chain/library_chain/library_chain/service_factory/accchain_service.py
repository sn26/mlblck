from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from library_chain.chain_factory import ChainFactory
from library_chain.wallets import Wallet
import time 
import requests
from library_chain.transactions import TransactionTypes
import json
import base64
import gzip
from library_chain.service_factory import ServiceTools
from library_chain.models import HashManager
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('transaction_b64')
parser.add_argument('signature')
parser.add_argument('block_hash')


'''
parser.add_argument( 'secret')
parser.add_argument( 'pk')
parser.add_argument( 'fee')
parser.add_argument( 'amount')
parser.add_argument( 'signature')
parser.add_argument( 'to')
parser.add_argument( 'digest')
parser.add_argument( 'timestamp')
parser.add_argument( 'TransactionType')
''' 
#Clase que implementa los servicios para el conteo de los usuarios (Wallets)
class AccChainService(Resource): 

    acc_chain = ChainFactory.create_chain(2)
    wallet = None #Antes de iniciar el servicio, los datos internos de la wallet no estarán disponibles dentro del servicio, necesitaremos tenerlos dentro de nuestra wallet

    
    peers = [] #Address to other participating on the network
    wallet = Wallet("ADM00")
    acc_chain.accounts.addresses.append( wallet.public_key )
    acc_chain.accounts.balance[wallet.public_key] = 0
    acc_chain.validators.balance[wallet.public_key] = 0
    acc_chain.validators.datasets[wallet.public_key] = []
    #acc_chain.validators.addresses.append(wallet.public_key)
    acc_chain.create_genesis_block(wallet) #Le pasamos la wallet para firmar el bloque

    #Añadimos una nueva transaccion (Lo tendremos que añadir a la nueva pool)
    #Cuando añadimos una nueva transacción, nos referimos a las que son de transferencia de dinero
    @app.route('/new_transaction', methods=['POST'])
    def add_transaction(  ): 
        args = parser.parse_args( )
        signature = ServiceTools.decode_signature( args["signature"])
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "fee", "amount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        return {"Success":201 ,  "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": args["fee"], 
            "amount": args["amount"], 
            "signature": args["signature"], 
            "to": args["to"], 
            "digest": args["digest"], 
            "timestamp": time.time(),
            "transaction": TransactionTypes.ADDTRANSACTION
        })}
       
    #Añadimos una nueva transaccion para añadir un nuevo validador a nuestra cadena 
    @app.route('/new_validator', methods=['POST'])
    def add_validator( ): 
        args = parser.parse_args( )
        signature = ServiceTools.decode_signature( args["signature"])
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "fee", "amount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        return {"Success":201 ,  "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": args["fee"], 
            "amount": args["amount"], 
            "signature": args["signature"], 
            "to": args["to"], 
            "validator_endpoint_address": args["address"], #Necesitamos guardarnos la direccion del validador
            "digest": args["digest"], 
            "timestamp": time.time(),
            "transaction": TransactionTypes.VALIDATOR
        })}
        
    

    #Añadimos un endpoint para añadir una nueva clave pública (acc) a nuestra cadena
    @app.route('/add_stake', methods=['POST'])
    def add_stake(  ): 
        args = parser.parse_args( )
        signature = ServiceTools.decode_signature( args["signature"])
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "fee", "amount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        return {"Success":201 ,  "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": args["fee"], 
            "amount": args["amount"], 
            "signature": args["signature"], 
            "to": args["to"], 
            "digest": args["digest"], 
            "timestamp": time.time(),
            "transaction": TransactionTypes.ADDSTAKE
        })}
        
    #Necesitamos añadir un campo que sea el numpy con los datos que vamos a añadir
    #Añadimos un endpoint para añadir una nueva clave pública (acc) a nuestra cadena
    @app.route('/add_valdata_stake', methods=['POST'])
    def add_dataset_to_staking_fc(  ): 
        args = parser.parse_args( )
        signature = ServiceTools.decode_signature( args["signature"])
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "fee", "amount", "signature", "to", "digest" , "data" ]:  
            if field not in args: 
                return "Invalid Transaction data", 404 
        return {"Success":201 ,  "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": args["fee"], 
            "amount": args["amount"], 
            "signature": args["signature"], 
            "data": args["data"], #Es necesario incluir la data de la transaccion (Data que usaremos para validar en las cadenas superiores)
            "to": args["to"], 
            "digest": args["digest"], 
            "timestamp": time.time(),
            "transaction": TransactionTypes.ADDVALDATASTAKE
        })}
       
    #Funcionando
    #Añadimos un endpoint para añadir una nueva clave pública (acc) a nuestra cadena
    @app.route('/new_account', methods=['POST'])
    def add_account( ): 
        args = parser.parse_args( )
        signature = ServiceTools.decode_signature( args["signature"])
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "fee", "amount", "signature", "to", "digest"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        return { "Success":201, "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": args["fee"], 
            "amount": args["amount"], 
            "signature": args["signature"], 
            "to": args["to"], 
            "digest": args["digest"], 
            "timestamp": time.time(),
            "transaction": TransactionTypes.ADDADDRESS
        }) }

    #FUNCIONANDO
    #Sacamos toda la info de los bloques de la cadena
    @app.route('/chain', methods=['GET'])
    def get_chain(): 
        chain_data = []
        for block in AccChainService.acc_chain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data),
                        "chain": chain_data,
                        "peers": list(AccChainService.peers)})
    
    
    #Funcionan (Probado sólo cuando somos validadores)
    #Endpoint para hacer que un validador nos firme un hash 
    @app.route('/sign', methods=["GET"])
    def sign():
        #Tenemos que comprobar que seamos los lideres 
        args =  parser.parse_args() 
        print( "NUESTROS ARGUMENTOS DE ENTRADA SON ")
        print(args)
        if ( args["block_hash"] == None ):
             
            return json.dumps( {
            "signature": "0"
        })
        #Si nuestro nodo es el validador de entre todos los nodos
        if AccChainService.acc_chain.get_leader( ) == AccChainService.wallet.public_key: 
            return json.dumps( {
                #Devolvemos la firma del bloque en ba64 
                "signature": HashManager.encode_signature(  AccChainService.wallet.sign(args["block_hash"])) 
            })
        #Si no somos el validador, enviamos al resto de los nodos para que alguno nos lo firme
        for node in AccChainService.peers: 
           
            response["signature"] = str( requests.get('{}/sign'.format(node) , params= args  ).json()) 
            if response["signature"] != "0": 
                return json.dumps( response)
        return json.dumps( {
            "signature": "0"
        })

    #ENDPOINT PARA SACAR EL DATASET DE UN VALIDADOR
    @app.route('/dataset' , methods=["GET"])
    def dataset(): 
        #Si nuestro nodo es el validador de entre todos los nodos
        if AccChainService.acc_chain.get_leader( ) == AccChainService.wallet.public_key: 
            return json.dumps( {
                "dataset": AccChainService.wallet.get_dataset()
            })
        #Si no somos el validador, enviamos al resto de los nodos para que alguno nos lo firme
        for node in AccChainService.peers: 
           
            response["dataset"] = str( requests.get('{}/dataset'.format(node)  ).json()) 
            if response["dataset"] != "0": 
                return json.dumps( response)
        return json.dumps( {
            "dataset": "0"
        })

    #FUNCIONANDO 
    #Minado de las transacciones que no se hayan confirmado aún (Necesitamos lanzar un endpoint para comprobar que funciona )
    @app.route('/mine', methods=['GET'])
    def mine():
        if len( AccChainService.acc_chain.unconfirmed_transactions ) == 0: 
            return {"Result": "No Transactions to mine."}
        result = AccChainService.acc_chain.mine() 
        print("NUESTRO RESULT ES ")
        print(result)
        if result == False: 
            return {"Result": "ERROR: Invalid transactions" }
        chain_length = len(AccChainService.acc_chain.chain) 
        print(" Estamos entrando para realizar el consenso con todas las peers ")
        if( AccChainService.consensus() == True):
            print("ESTAMOS ENTRANDO")
            AccChainService.acc_chain.unconfirmed_transactions.clear() #Limpiamos las transacciones una vez hemos minado el bloque
            return {"Result": "Consesus from another node. No block mined but chain changed", "Chain": AccChainService.get_chain() } 
        if chain_length == len(AccChainService.acc_chain.chain):
            # announce the recently mined block to the network
            print("ESTAMOS ENTRANDO A ANUNCIAR UN BLOQUE")
            AccChainService.announce_new_block(AccChainService.acc_chain.last_block)
        AccChainService.acc_chain.unconfirmed_transactions.clear() #Limpiamos las transacciones una vez hemos minado el bloque
        return {"Result": "Block #{} is mined.".format(AccChainService.acc_chain.last_block.index) }

    #Endpoint to add AccChainService.peers 
    @app.route('/register_node', methods=['POST']) 
    def register_peer():
        node_address = request.get_json()["node_address"]
        if not node_address: 
            return "ERROR: Invalid data" 
        AccChainService.peers.add( node_address )
        return self.get_chain()
    
    @app.route('/register_with' , methods= ['POST'])
    def register_with_existing_node( ): 
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
            AccChainService.acc_chain = create_chain_from_dump(chain_dump)
            #Nos añadimos a la chain
            AccChainService.peers.append(response.json()['peers'])
            return "Registration successful", 200
        else:
            # if something goes wrong, pass it on to the API response
            return response.content, response.status_code
    
    #FUNCIONANDO
    @app.route('/get_leader', methods=["GET"])
    def get_leader( ): 
        return  {"Result": AccChainService.acc_chain.validators.rest_addresses[AccChainService.acc_chain.get_leader() ] }


    @app.route('/add_block', methods=["POST"])
    def verify_and_add_block(): 
        block_data = request.get_json()
        block = Block(block_data["index"],
                    block_data["transactions"],
                    block_data["timestamp"],
                    block_data["previous_hash"],
                    block_data["nonce"], 
                    block_data["pk"])
        if ( AccChainService.acc_chain.add_block(block ) == False): 
            return "The block was discarded by the node", 400
        return "Block added to the chain", 201
    
    #FUNCIONANDO
    @app.route('/pending_transactions', methods=["GET"])
    def get_pending_transactions(): 
        res = []
        for transaction in AccChainService.acc_chain.unconfirmed_transactions : 
            res.append( HashManager.delete_unnecesary_params_from_transaction( transaction ))
        return {"Success":201, "Result": res }
        
    #FUNCIONANDO
    #Function to create a new wallet
    @app.route('/wallet', methods=["POST"]) 
    def create_wallet(): 
        args =  parser.parse_args()
        print( args)
        AccChainService.wallet = Wallet( args['secret']  )
        return {"WalletValues": AccChainService.wallet.toString() }

    #Funcionando    
    #Endpoint para sacar el balance de los históricos de las transacciones
    @app.route('/get_history_balance' , methods=["GET"])
    def get_history_balance(  ): 
        return {"Result": AccChainService.acc_chain.accounts.balance }

    #Sacamos los validadores que tenemos almacenados (Necesario para el resto de las chains)
    @app.route('/validators' ,methods=['GET'])
    def get_validators( ): 
        return {"validators": AccChainService.acc_chain.validators.rest_addresses}
    
    def set_new_validator( self): 
        print("Seteamos un nuevo validador inicial")
        AccChainService.acc_chain.validators.validators.append(AccChainService.wallet.public_key)
        AccChainService.acc_chain.validators.balance[AccChainService.wallet.public_key] = 100
        AccChainService.acc_chain.validators.datasets[AccChainService.wallet.public_key] = []
        AccChainService.acc_chain.validators.rest_addresses[AccChainService.wallet.public_key] = "http://127.0.0.1:12345/"
        return 

    def set_user_chain( self, url): 
        #Seteamos la url del usuario, para las requests que se hace en común, aunque en este caso realmente no haría falta
        AccChainService.acc_chain.set_user_chain( url  )
        return

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

    def generate_encoded_transaction_and_signature_for_test(self ): 
        
        transaction = {"fee": 0 , "transaction": "addAddress" , "amount": 0 ,
         "pk": AccChainService.wallet.public_key, "signature":"0" , "timestamp": 0 ,
          "to": AccChainService.wallet.public_key , "digest": 0 }
        signature = base64.encodebytes( AccChainService.wallet.signTransaction( transaction ) ).decode("utf-8")
        #codificamos la transaccion y la firma
        res = base64.encodebytes( bytes( json.dumps( str( transaction))  , "utf-8" ) ).decode("utf-8")
        compression = gzip.compress( bytes ( json.dumps( res) , "utf-8" )  )
        return base64.encodebytes( compression).decode("utf-8"), signature

    #FUNCIONANDO CUANDO NO HAY PEERS (AHORA, AÑADIREMOS UNA PEER SIN DATOS Y OTRA CON UN NUM MAYOR DE TRANSACCIONES A LAS NUESTRAS)
    def consensus( ): 
        global acc_chain
        longest_chain = None 
        current_len = len(AccChainService.acc_chain.chain)
        print("ESTAMOS PASANDO A REALIZAR EL CONSENSO")
        for node in AccChainService.peers:
            response = requests.get('{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            print("NUESTRA LEN ACTUAL ES ")
            print( current_len)
            print("LA LEN QUE HEMOS SACADO DE LA CHAIN ES ")
            print(length )#No se saca bien la length de la otra chain!! REVISAR 
            print("LA VAL DE LA CHAIN ES ")
            print( AccChainService.acc_chain.check_chain_validity(chain))
            if length > current_len and AccChainService.acc_chain.check_chain_validity(chain) == True:
                print("HEMOS ENTRADO Y ESTAMOS PONIENDO LA VAL DE LA CHAIN")
                current_len = length
                longest_chain = chain
        print(" HEMOS SACADO EL CONSENSO")
        if longest_chain != None:
            print("ESTAMOS CAMBIANDO NUESTRA CHAIN")
            AccChainService.acc_chain = longest_chain
            return True
        return False
    
    def announce_new_block( block ): 
        for peer in AccChainService.peers:
            url = "{}add_block".format(peer)
            headers = {'Content-Type': "application/json"}
            requests.post(url,
                        data=json.dumps(block.__dict__, sort_keys=True),
                        headers=headers)

    def launchme( self , host , port): 
        #api.add_resource(AccChainService , '/UserChain')
        app.run( host= host , port=port, debug =False )





if __name__ == "__main__":
    print("ESTAMOS LANZANDO EL MAIN")    