from library_server.chain_factory import ChainFactory
from library_server.models import Block
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('data_img' )


  
class  RootChainEndpoint(Resource): 

    def __init__(self ) :
        print("PASAMOS")
        self.model = ModelTrained() 
        self.srvCnn = ServerCnn(ModelWeights.weights, self.model  )
        print("PASAMOS")
        return

    @app.route('/new_transaction', methods=['POST'] )
    def new_transaction( self  ):
        tx_data = request.get_json()
        for field in  ["weights", "model_arch"]:
            if not tx_data.get(field):
                return "Invalid transaction data", 404
        tx_data["timestamp"] = time.time()
        try: 
            blockchain.add_new_transaction(tx_data)
            return "Success", 200
        except Exception as e: 
            return "Bad Request", 400
    
    #Endpoint to get a block by hash
    @app.rout("/get_block", methods=["GET"])
    def get_block(self): 
        tx_data = request.get_json()
        return self.rchain.get_block_by_hash(tx_data.get("hash")) 





##
## Setting up the resource routing
api.add_resource(ServerEndpoint , '/LogDetection')
app.run( debug =True )

    