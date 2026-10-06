# from .block import Block_bluePrint
# from .blockChain import BlockChain

# bc = BlockChain()

# bc.add_tranxn("JntuH", "Nirupam", "B.Tech CSE")
# bc.insert_block("JntuH")
# bc.add_tranxn("JntuS", "Arjun", "B.Tech CSE")
# bc.insert_block("JntuS")

# for x in bc.chain:
#     print("Index : ", x.index)
#     print("Data : ", x.data)
#     print("Current Block Hash : ", x.hash)
#     print("Prev Block hash : ", x.prevBlockHash)
#     print('-' * 40)
# # bc.chain[1].data[0]["receiver"] = "Hackerz"

# cert_hash = bc.chain[1].data[0]["certificate_hash"]

# result = bc.search_by_hash(cert_hash)

# print("Search result:", result)

# print(bc.is_chain_valid())