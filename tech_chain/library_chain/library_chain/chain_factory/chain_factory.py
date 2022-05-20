from library_chain.chain_factory import MainChain
from library_chain.chain_factory import RootChain
from library_chain.chain_factory import AccManagerChain

class ChainFactory: 

    @staticmethod
    def create_chain( id ): 
        if id == 0: 
            return MainChain() 
        elif id == 1 : 
            return RootChain( )
        elif id ==2 : 
            return AccManagerChain( )

   