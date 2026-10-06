import json
import hashlib
import time

class Block_bluePrint:

    def __init__(self, index :int, prevBlockHash :str, data, issuer:str):

        self.index = index
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.data = data
        self.prevBlockHash = prevBlockHash
        self.issuer = issuer

        self.hash = self.compute_block_hash()
    

    def compute_block_hash(self):
        
        block_data = {

            "index" : self.index,
            "timestamp" : self.timestamp,
            "issuer" : self.issuer,
            "data" : self.data,
            "prevBlockHash" : self.prevBlockHash

        }

        blockData_inString = json.dumps(block_data, sort_keys=True)

        hashFor_thisBlock = hashlib.sha256(blockData_inString.encode()).hexdigest()

        return hashFor_thisBlock
    
    #for serializing i.e python obj to JSON format...
    def to_dict(self):

        return {
        "index": self.index,
        "timestamp": self.timestamp,
        "issuer": self.issuer,
        "data": self.data,
        "prevBlockHash": self.prevBlockHash,
        "hash": self.hash
    }
    
    
