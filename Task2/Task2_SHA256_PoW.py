import hashlib
import json
import os

def compute_SHA256_hash(raw_data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(raw_data.encode('utf-8'))
    return sha256_hash.hexdigest()


def mine_block(previous_block, data):
    nonce = 0
    while True:
        hash_input = data + str(nonce)
        hashed_data = compute_SHA256_hash(hash_input)
        if hashed_data.startswith("0000"):
            return {
                'data': data,
                'hash': hashed_data,
                'nonce': nonce,
                'previous_hash': previous_block['hash']
            }
        nonce += 1


def save_block(block, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            blockchain = json.load(file)
    else:
        blockchain = []

    if len(blockchain) == 0:
        block['previous_hash'] = '0'
    else:
        block['previous_hash'] = blockchain[-1]['hash']

    blockchain.append(block)

    with open(file_path, 'w') as file:
        json.dump(blockchain, file, indent=4)


def verify_last_block(file_path):
    with open(file_path, 'r') as file:
        blockchain = json.load(file)

    last_block = blockchain[-1]
    hash_input = last_block['data'] + str(last_block['nonce'])
    hashed_data = compute_SHA256_hash(hash_input)

    if hashed_data.startswith("0000") and hashed_data == last_block['hash']:
        print("Last block verified successfully.")
        return True
    else:
        print("Verification failed.")
        return False

if __name__ == "__main__":
    start_block = {
        'data': "Block 0",
        'hash': "0000bd72330f5b50e0f26608d75df391b7408e530dd5dad6205fa22917de5d43",
        'nonce': 139844,
        'previous_hash': ""
    }

    file_path = '/home/jackie/uni/Blockchain/blockchain.json'
    save_block(start_block, file_path)

    previous_block = start_block
    for i in range(3):
        verify_last_block(file_path)
        new_data = f"Block {i+1}"
        new_block = mine_block(previous_block, new_data)
        save_block(new_block, file_path)
        previous_block = new_block