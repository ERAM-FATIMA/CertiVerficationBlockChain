from .block import Block_bluePrint
import json, os

class BlockChain:

    def __init__(self):
        
        self.chain = []
        self.pending_tranxns = []
        #self.authorized_issuers = ["JntuS", "JntuH", "JntuK", "IITH"]
        self.storage_path = os.path.join(os.path.dirname(__file__), "blockchain_storage.json")
        self.load_chain()
        
        self.rebuild_hash_map()  #just for restoring hash map in memory, since it keeps on resetting for server start and off...


    def create_genericBlock(self):

        generic_block = Block_bluePrint(
            index = 0,
            issuer = "ROOT_AUTHORITY",
            prevBlockHash = "0",  #since it is the starting block, so prev hash = "0"...
            data = "Generic Block Hereeee!!"
        )
        
        self.chain.append(generic_block)
        return True
    
    def add_tranxn(self, issuer, receiver, certi_id, certi_hash):

        tranxn = {
            "certificate_id" : certi_id,
            "issuer" : issuer,
            "receiver" : receiver,
            "certificate_hash" : certi_hash
        }

        self.pending_tranxns.append(tranxn)
    
    def insert_block(self, issuer):

        # if self.validate_issuer(issuer):

            if self.check_pending_pool():

                last_block:Block_bluePrint = self.get_last_block()

                new_block_toAdd = Block_bluePrint(

                    index = len(self.chain),
                    issuer = issuer,
                    data = self.pending_tranxns,
                    prevBlockHash = last_block.hash
                )

                self.chain.append(new_block_toAdd)
                #simply storing newly added block's hash into hashmap with index for easy access..
                # cert_hash <-> block_index map created for O(1) access!!
                for txn in self.pending_tranxns:
                    cert_hash = txn["certificate_hash"]
                    self.hash_index[cert_hash] = new_block_toAdd.index

                self.pending_tranxns = []   #reset all pending Transxns...

                
                self.save_chain()
                return new_block_toAdd.index
        # return
    
    def is_chain_valid(self):

        #valid conditions :
            #1. the generated hash during block creation == now re-computed hash
            #2. the curBlock.prevBlockhash == prevBlock.actualHash....

        for i in range(1, len(self.chain)):

            cur_block: Block_bluePrint = self.chain[i]
            prev_block: Block_bluePrint = self.chain[i-1]

            if cur_block.hash != cur_block.compute_block_hash():
                print("hash altered for block : ", cur_block.index)
                print("Actual hash stored = ", cur_block.hash)
                print("Hash computed now : ", cur_block.compute_block_hash())
                return {
                    "block_altered" : cur_block.index,
                    "actual_hash" : cur_block.hash,
                    "hash_computed_now" : cur_block.compute_block_hash()
                }
            
            if cur_block.prevBlockHash != prev_block.hash:
                return False
        
        return True
    
    def get_last_block(self):

        last_block = self.chain[-1]
        return last_block
    
    # def validate_issuer(self, issuer):

    #     if issuer not in self.authorized_issuers:
    #         print(f'{issuer} not authorized!')
    #         print(f'{self.pending_tranxns} not inserted!')
    #         return False
        
    #     return True
    
    def check_pending_pool(self):
        
        if not self.pending_tranxns:
            print("No pending tranxns to update chain...!")
            return False
        
        return True
    
    #deserialization..i.e JSON to Python objects..        
    def load_chain(self):

        if not os.path.exists(self.storage_path):
            self.create_genericBlock()
            self.save_chain()
            return
        
        with open(self.storage_path, "r") as f:
            data_from_load:dict = json.load(f)
        
        if not data_from_load:
            self.create_genericBlock()
            self.save_chain()
            return
        
        #building the chain from stored json file... but we create object again because
        #we dont simply want the text format. we want them in accessesible objects for accessing its methods...

        for block in data_from_load:
            block_block = Block_bluePrint(
                index= block["index"],
                prevBlockHash= block["prevBlockHash"],
                data= block["data"],
                issuer = block["issuer"],
            )
            
            #but the time stamp and hash must be same, so we are using the same old values from json...
            block_block.timestamp = block["timestamp"]
            block_block.hash = block["hash"]

            self.chain.append(block_block)
    
    #serialization..i.e python objects to JSON format..
    def save_chain(self):

        chain_data = []
        block :Block_bluePrint

        for block in self.chain:
            chain_data.append(block.to_dict())
        
        with open(self.storage_path, "w") as f:
            json.dump(chain_data, f, indent=4)


    # def search_by_hash(self, cert_hash:str): ## O(n) complexity method for verifying...

    #     block: Block_bluePrint

    #     for block in self.chain:
            
    #         if block.index == 0:
    #             continue

    #         for record in block.data:

    #             if record["certificate_hash"] == cert_hash:
    #                 return{
    #                     "block_index": block.index,
    #                     "certificate_file": record
    #                 }
        
    #     return None

    def verify_certificate(self, in_cert_hash):

        flag_bit = self.is_chain_valid()
        if flag_bit is True:

            if in_cert_hash in self.hash_index:
                block_index = self.hash_index[in_cert_hash]
                return{
                    "status" : "VALID",
                    "block_index" : block_index
                }
        
            return{
                "status" : "INVALID"
            }
        return flag_bit
    
    def rebuild_hash_map(self):
        self.hash_index = {}
        block: Block_bluePrint
        for block in self.chain:

            if block.index == 0:
                continue
            for txn in block.data:
                cert_hash = txn["certificate_hash"]

                self.hash_index[cert_hash] = block.index