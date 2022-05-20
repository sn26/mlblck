from library_chain.proof_factory import ProofOfLearning
#from library_chain.proof_factory import ProofOfStake

class ProofFactory: 

    @staticmethod
    def create_proof(id) :
            return ProofOfLearning() 
