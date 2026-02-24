import hashlib

class HashDataBlock:
    def __init__(self, previous_block_hash, data_list):
        self.previous_block_hash = previous_block_hash
        self.data_list = data_list
        self.block_data = "-".join(data_list) + "-" + previous_block_hash
        self.block_hash = hashlib. sha256(self.block_data.encode()).hexdigest()
