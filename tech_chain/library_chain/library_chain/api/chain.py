

class Chain: 

    def __init__(self): 
        self.size_per_block = 1000 
        self.blocks = []
        return
    
   


    def add_block(self, block):
        if self.blocks[-1].hash != block.previous_hash:
            return False
        self.blocks.append(block)
