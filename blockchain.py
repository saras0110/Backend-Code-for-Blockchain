import json, hashlib, time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, 'Genesis Block', '0')

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), data, last_block.hash)
        self.chain.append(new_block)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([block.__dict__ for block in self.chain], f)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                chain_data = json.load(f)
                self.chain = [Block(**block) for block in chain_data]
        except FileNotFoundError:
            self.chain = [self.create_genesis_block()]

    def count_votes(self):
        votes = {}
        for block in self.chain[1:]:
            party = block.data['vote']
            votes[party] = votes.get(party, 0) + 1
        return votes
