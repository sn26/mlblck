from library_chain.proof_factory import ProofOfLearning
from library_chain.proof_factory import ProofOfStake

class ProofFactory: 

    def __init__(self, chain_id):
        self.chain_id = chain_id
        return 

    def create_proof(self):
        if self.chain_id == 0: 
            return ProofOfLearning()
        else: 
            return ProofOfStake() 
