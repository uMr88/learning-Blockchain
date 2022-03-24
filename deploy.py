from traceback import print_tb
from solcx import compile_standard, install_solc

install_solc("0.6.0")
import json
from web3 import Web3
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi", "metadata", "evm.bytecode",
                        "evm.bytecode.sourceMap"
                    ]
                }
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
# to deploy
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"][
    "evm"]["bytecode"]["object"]

# get abi
abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]
                 ["SimpleStorage"]["metadata"])["output"]["abi"]
# FOR Conecting to ganche
w3 = Web3(Web3.HTTPProvider("URL"))
chain_id = 1337
my_address = "0x9235436774444444444447944Ea8c9C1"
private_key = "0xR4534G54Y45Y4Y4Y4"
# create the contract python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)
nonce = w3.eth.getTransactionCount(my_address)
#1.Build a transcation 2. sign 3. send
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce
})
# print(transaction)
signed_txn = w3.eth.account.sign_transaction(transaction,
                                             private_key=private_key)
# print(signed_txn)
# Send this signed txn
print("Deploying cotract ....")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!!!! ....")
# WORKING WITH CONTRACT
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())
print("Updating contract....")
greeting_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId":
    chain_id,
    "gasPrice":
    w3.eth.gas_price,
    "from":
    my_address,
    "nonce":
    nonce + 1,
})
signed_greeting_txn = w3.eth.account.sign_transaction(greeting_transaction,
                                                      private_key=private_key)
tx_greeting_hash = w3.eth.send_raw_transaction(
    signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print("Updated contract!!!....")

print(simple_storage.functions.retrieve().call())
