from library_chain.chain_factory import ChainFactory
from library_chain.models import BlockSerializer

class ChainSerializer: 

    @staticmethod
    def serialize_acc_chain( chain ): 
        #La chain nos trae los bloques en una lista, por lo que tendremos que crearnos una chain
        acc_chain = ChainFactory.create_chain(2)
        for i in range( 0, len(chain)): 
            acc_chain.chain.append(BlockSerializer.serialize( chain[i]))
            acc_chain.execute_block( ) #Actualizamos las accounts y demas, a lo que deberian de tener
        return  acc_chain
