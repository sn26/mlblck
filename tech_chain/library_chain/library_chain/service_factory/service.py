
class Service: 

    @staticmethod 
    def get_chain(id): 
        if id == 0: 
            from library_chain.service_factory import MainChainService
            return MainChainService()
        else: 
            from library_chain.service_factory import RootChainService
            return RootChainService()
        return None




