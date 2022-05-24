from library_chain.models import Block

class BlockSerializer: 

    @staticmethod
    def serialize( block ): 
        blck = Block( block["index"] , block["neural_data_transaction"], block["timestamp"], block["previous_hash"], block["validator"] ) 
        blck.timestamp = block["timestamp"]
        blck.nonce = block["nonce"]
        blck.model = block["model"]
        blck.validator = block["validator"]
        blck.signature = block["signature"]
        blck.hash = block["hash"]
        return blck