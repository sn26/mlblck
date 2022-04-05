from library_chain.chain_factory import MainChain
from library_chain.chain_factory import RootChain

class ChainFactory: 

    @staticmethod
    def create_chain( id ): 
        if id == 0: 
            return MainChain(id) 
        else: 
            return RootChain(id, 1 )

   