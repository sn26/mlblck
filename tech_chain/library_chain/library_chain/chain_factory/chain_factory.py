from library_chain.chain_factory import MainChain
from library_chain.chain_factory import RootChain
from library_chain.chain_factory import AccManagerChain

class ChainFactory: 

    @staticmethod
    def create_chain( id ): 
        if id == 0: 
            return MainChain() 
        else if id == 1 : 
            return RootChain( )
        else if id ==2 : 
            return AccManagerChain( )

   