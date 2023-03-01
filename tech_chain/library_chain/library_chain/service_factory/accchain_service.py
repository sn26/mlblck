from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from library_chain.chain_factory import ChainFactory, ChainSerializer
from library_chain.wallets import Wallet
import time 
import requests
from library_chain.transactions import TransactionTypes
import json
import base64
import gzip
from library_chain.service_tools import ServiceTools
from library_chain.models import BlockSerializer
from library_chain.models import HashManager
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('transaction_b64')
parser.add_argument('signature')
parser.add_argument('block_hash')
parser.add_argument('node_address') #Lo utilizaremos como param para añadir nodos a nuestra cadena
parser.add_argument('pk') #Pk que usaremos para la ico
parser.add_argument('dataset') #Pk que usaremos para la ico



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
   
    peers = set() #Address to other participating on the network
   
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
            "fee": int( args["fee"]), 
            "amount": int( args["amount"]), 
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
        for field in ["pk", "fee", "amount", "signature", "to", "digest" ,  "validator_endpoint_address", "dataset"]: 
            if field not in args: 
                return "Invalid Transaction data", 404 
        return {"Success":201 ,  "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": int( args["fee"]) , 
            "amount": int( args["amount"] ), 
            "dataset": args["dataset"], 
            "signature": args["signature"], 
            "to": args["to"], 
            "validator_endpoint_address": args[ "validator_endpoint_address"], #Necesitamos guardarnos la direccion del validador
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
            "fee": int( args["fee"] ), 
            "amount": int( args["amount"] ), 
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
        if args["dataset"] == None: 
            return "Invalid Transaction data", 404
        signature = ServiceTools.decode_signature( args["signature"])
        dataset = args["dataset"] 
        args = ServiceTools.decode_transaction( args["transaction_b64"]) #Decodificamos la transaccion que nos viene en base 64 
        args["signature"] = signature
        #Una vez tenemos la transaccion, sacamos  la firma 
        for field in ["pk", "fee", "amount", "signature", "to", "digest" , "dataset" ]:  
            if field not in args: 
                return "Invalid Transaction data", 404 
        print("El dataset que tenemos ahora es ")
        print(json.loads( dataset))
        return {"Success":201 ,  "Result":  AccChainService.acc_chain.add_new_transaction({
            "pk": args["pk"], 
            "fee": int( args["fee"]), 
            "amount": int( args["amount"] ), 
            "signature": args["signature"], 
            "dataset": json.loads( dataset ), #Es necesario incluir la data de la transaccion (Data que usaremos para validar en las cadenas superiores)
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
            "fee": int( args["fee"]), 
            "amount":int( args["amount"]), 
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
            chain_data.append(block.to_string())
        return json.dumps({"length": len(chain_data),
                        "chain": chain_data,
                        "peers": list( AccChainService.peers) })
    
    
    #Funcionan (Probado sólo cuando somos validadores)
    #Endpoint para hacer que un validador nos firme un hash 
    @app.route('/sign', methods=["GET"])
    def sign():
        #Tenemos que comprobar que seamos los lideres 
        args =  parser.parse_args() 
        if ( args["block_hash"] == None ):
             
            return json.dumps( {
            "signature": "0"
        })
        #Si nuestro n odo es el validador de entre todos los nodos
       
        if AccChainService.acc_chain.get_leader( ) == AccChainService.acc_chain.wallet.public_key: 
            return json.dumps( { 
                #Devolvemos la firma del bloque en ba64 
                "signature": HashManager.encode_signature(  AccChainService.acc_chain.wallet.sign(args["block_hash"])) 
            })
        print("EL LEADER QUE TENEMOS EN NUESTRA CHAIN ES ")
        print(AccChainService.acc_chain.get_leader( ) )
        print("LA WALLET QUE TENEMOS ES")
        print( AccChainService.acc_chain.wallet.public_key)
        #Si no somos el validador, enviamos al resto de los nodos para que alguno nos lo firme
        #for validator in AccChainService.acc_chain.validators.rest_addresses.keys(): 
        #if request.host_url != AccChainService.acc_chain.validators.rest_addresses[validator]:
        response = requests.get('{}/sign'.format(AccChainService.acc_chain.validators.rest_addresses[AccChainService.acc_chain.get_leader() ]) , params= args  ).json()
        #if response["signature"] != "0": 
        #print("ESTAMOS ENTRANOD A DEVOLVER LA FIRMA")
        #print(response)
        return json.dumps( response)
        '''
        return json.dumps( {
            "signature": "0"
        })
        '''

    #ENDPOINT PARA SACAR EL DATASET DE UN VALIDADOR
    @app.route('/dataset' , methods=["GET"])
    def dataset(): 
        #Si nuestro nodo es el validador de entre todos los nodos
        if AccChainService.acc_chain.get_leader() != None: 
            return json.dumps( {
                "dataset": AccChainService.acc_chain.validators.datasets[AccChainService.acc_chain.get_leader()]
            })
        #Si no somos el validador, enviamos al resto de los nodos para que alguno nos lo firme
        for node in AccChainService.peers: 
           
            response = str( requests.get('{}/dataset'.format(node)  ).json()) 
            if response["dataset"] != []: 
                return json.dumps( response)
        return json.dumps( {
            "dataset": []
        })

    #FUNCIONANDO 
    #Minado de las transacciones que no se hayan confirmado aún (Necesitamos lanzar un endpoint para comprobar que funciona )
    @app.route('/mine', methods=['GET'])
    def mine():
        if len( AccChainService.acc_chain.unconfirmed_transactions ) == 0: 
            return {"Result": "No Transactions to mine."}
        print("HEMOS ENTRADO A MINAR Y EL LEADER QUE SACAMOS ES ")
        print(AccChainService.acc_chain.get_leader( ))
        result = AccChainService.acc_chain.mine() 
        if result == False: 
            AccChainService.acc_chain.unconfirmed_transactions.clear() #Limpiamos el conjunto de transacciones con las que contaba la chain
            return {"Result": "ERROR: Invalid transactions" }
        chain_length = len(AccChainService.acc_chain.chain) 
        #return {"Result": "Evitamos el consenso"}
        print(" Estamos entrando para realizar el consenso con todas las peers ")
        if( AccChainService.consensus() == True):
            #AccChainService.acc_chain.unconfirmed_transactions.clear() #Limpiamos las transacciones una vez hemos minado el bloque
            return {"Result": "Consesus from another node. No block mined but chain changed", "Chain": AccChainService.get_chain() } 
        if chain_length == len(AccChainService.acc_chain.chain):
            # announce the recently mined block to the network
            AccChainService.announce_new_block(AccChainService.acc_chain.last_block)
        AccChainService.acc_chain.unconfirmed_transactions.clear() #Limpiamos las transacciones una vez hemos minado el bloque
        return {"Result": "Block #{} is mined.".format(AccChainService.acc_chain.last_block.index) }

    #Funcionando
    #Endpoint to add AccChainService.peers 
    @app.route('/register_node', methods=['POST']) 
    def register_peer():
        node_address = request.get_json()["node_address"]
        if node_address == None:  
            return "ERROR: Invalid data" , 400 
        AccChainService.peers.add( request.host_url ) #Nos concatenamos a nosotros mismos 
        AccChainService.peers.add( node_address )
        return AccChainService.get_chain()
    
    #Funcionando
    @app.route('/register_with' , methods= ['POST'])
    def register_with_existing_node( ): 
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
            AccChainService.acc_chain = AccChainService.create_chain_from_dump(chain_dump )
            #Nos añadimos a la chain
            for i in range( 0 , len( response.json()['peers'])):
                AccChainService.peers.add(response.json()['peers'][i]) #Concatenamos las peers en nuestra lista
            return "Registration successful", 200
        else:
            # if something goes wrong, pass it on to the API response
            return response.content, response.status_code
    
    #FUNCIONANDO
    @app.route('/get_leader', methods=["GET"])
    def get_leader( ): 
        return  {"leader":  AccChainService.acc_chain.get_leader()  , "rest": AccChainService.acc_chain.validators.rest_addresses[AccChainService.acc_chain.get_leader() ] }


    @app.route('/add_block', methods=["POST"])
    def verify_and_add_block(): 
        block_data = request.get_json()
        block = BlockSerializer.serialize( block_data)
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
        AccChainService.acc_chain.wallet = Wallet( args['secret']  )
        return {"WalletValues": AccChainService.acc_chain.wallet.toString() }

    #Funcionando    
    #Endpoint para sacar el balance de los históricos de las transacciones
    @app.route('/get_history_balance' , methods=["GET"])
    def get_history_balance(  ): 
        return {"Result": AccChainService.acc_chain.accounts.balance }

    #Sacamos los validadores que tenemos almacenados (Necesario para el resto de las chains)
    @app.route('/validators' ,methods=['GET'])
    def get_validators( ): 
        return {"validators": AccChainService.acc_chain.validators.rest_addresses}

    #Function thath creates some wallet with balance in acc 
    @app.route('/ico' ,methods=['POST'])
    def ico( ): 
        if len( AccChainService.acc_chain.chain ) != 1:
            return "ERROR: Chain already initialized", 400
        if len(AccChainService.acc_chain.unconfirmed_transactions) != 1: 
            return  "ERROR: Chain already initialized", 400
        args =  parser.parse_args()
        
        #Esta parte de aqui en realidad la podriamos quitar 
        #Lo que haremos será añadir una serie de transacciones al principio, añadiendo las wallets que queramos, y que van a recibir el stake suficiente para poder validar, serán nuestros nodos principales validadores
        transaction = {"fee": 0 , "amount": 200,
         "pk": AccChainService.acc_chain.wallet.public_key, "signature":"0" , "timestamp": 0 ,
          "to": args["pk"] , "digest": 0 }
        signature = base64.encodebytes( AccChainService.acc_chain.wallet.signTransaction( transaction ) ).decode("utf-8")
        #codificamos la transaccion y la firma
        res = base64.encodebytes( bytes( json.dumps( str( transaction))  , "utf-8" ) ).decode("utf-8")
        compression = gzip.compress( bytes ( json.dumps( res) , "utf-8" )  )
        headers = {'Content-Type': "application/json"}
        #AccChainService.set_new_validator( ) #Seteamos nuevamente el validador con el que hemos firmado la transaccion para conseguir persistir las 100 coins
        return {"Success": 201 , "Result":str(requests.post(request.host_url+ "/new_transaction",
                    data=json.dumps({"transaction_b64":  base64.encodebytes( compression).decode("utf-8") , "signature": signature}),
                    headers=headers).content) }
    
   
    @staticmethod 
    def create_chain_from_dump( chain_dump): 
        
        AccChainService.acc_chain = ChainSerializer.serialize_acc_chain( chain_dump, AccChainService.acc_chain.wallet ) #Serializamos la chain de los usuarios, para que coincida con lo que tenemos interno
        
        return AccChainService.acc_chain

    ''' 
    def generate_encoded_transaction_and_signature_for_test(self ): 
        
        transaction = {"fee": 0 , "transaction": "addAddress" , "amount": 0 ,
         "pk": AccChainService.acc_chain.wallet.public_key, "signature":"0" , "timestamp": 0 ,
          "to": AccChainService.acc_chain.wallet.public_key , "digest": 0 }
        signature = base64.encodebytes( AccChainService.acc_chain.wallet.signTransaction( transaction ) ).decode("utf-8")
        #codificamos la transaccion y la firma
        res = base64.encodebytes( bytes( json.dumps( str( transaction))  , "utf-8" ) ).decode("utf-8")
        compression = gzip.compress( bytes ( json.dumps( res) , "utf-8" )  )
        return base64.encodebytes( compression).decode("utf-8"), signature
    ''' 

    #FUNCIONANDO CUANDO NO HAY PEERS (AHORA, AÑADIREMOS UNA PEER SIN DATOS Y OTRA CON UN NUM MAYOR DE TRANSACCIONES A LAS NUESTRAS)
    def consensus( ): 
        longest_chain = None 
        current_len = len(AccChainService.acc_chain.chain)
        for node in AccChainService.peers:
            print("Nuestros nodos son ")
            print( node)
            response = requests.get('{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            print("LA CHAIN QUE ESTAMOS PROBANDO ES ")
            print(chain)
            print("LA LENGTH QUE TENEMOS DE LA CHAIN ES ")
            print(length)
            print("NUESTRA LEN ACTUAL ES ")
            print(current_len)
            print("CUANDO COMPROBAMOS LA VAL DE LA CHAIN NOS DA ")
            print(AccChainService.acc_chain.check_chain_validity(chain))
            if length > current_len and AccChainService.acc_chain.check_chain_validity(chain) == True:
                current_len = length
                longest_chain = chain
        print(" HEMOS SACADO EL CONSENSO")
        if longest_chain != None:
            print("ESTAMOS CAMBIANDO NUESTRA CHAIN!!!!!!!!!!!!!!!")
            #AccChainService.acc_chain.wallet_setup( )
            #AccChainService.set_new_validator() #Seteamos nuevamente nuestra wallet como validadora
            AccChainService.acc_chain = ChainSerializer.serialize_acc_chain( longest_chain ) #Serializamos la chain de los usuarios, para que coincida con lo que tenemos interno
            
            return True
        return False
        

    def announce_new_block( block ): 
        for peer in list( AccChainService.peers):
            url = "{}/add_block".format(peer)
            headers = {'Content-Type': "application/json"}
            requests.post(url,
                        data=json.dumps(block.to_string(), sort_keys=True),
                        headers=headers)

    def launchme( self , host , port ): 
        #api.add_resource(AccChainService , '/UserChain')
        #AccChainService.acc_chain.wallet_setup( )
        AccChainService.acc_chain.create_genesis_block(AccChainService.acc_chain.wallet) #Le pasamos la wallet para firmar el bloque
        app.run( host= host , port=port, debug =False )
       






if __name__ == "__main__":
    
    print("ESTAMOS LANZANDO EL MAIN")    