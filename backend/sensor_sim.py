import time
from web3 import Web3

# 1. Connect to Local Hardhat Blockchain
# Hardhat always runs on this URL
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 2. CONFIGURATION
# ------------------------------------------------------
# PASTE YOUR DEPLOYED ADDRESS HERE! vvvvv
CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3' 
# ------------------------------------------------------

# We use the first "Fake Account" provided by Hardhat to sign transactions
SENDER_ADDRESS = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
SENDER_PRIVATE_KEY = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

# 3. The ABI (The "Manual" for the contract)
# This tells Python what functions exist.
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "uint256", "name": "_price", "type": "uint256"}
        ],
        "name": "createBatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_batchId", "type": "uint256"},
            {"internalType": "uint256", "name": "_temp", "type": "uint256"}
        ],
        "name": "updateTemperature",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "batchId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "newPrice", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "temperature", "type": "uint256"}
        ],
        "name": "PriceUpdated",
        "type": "event"
    }
]

# Initialize Contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def send_transaction(func_call):
    # 1. Build the transaction
    tx = func_call.build_transaction({
        'from': SENDER_ADDRESS,
        'nonce': w3.eth.get_transaction_count(SENDER_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.to_wei('10', 'gwei')
    })
    
    # 2. Sign it with the private key
    signed_tx = w3.eth.account.sign_transaction(tx, SENDER_PRIVATE_KEY)
    
    # 3. Send it to the network
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction Sent! Hash: {tx_hash.hex()}")
    
    # 4. Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def main():
    if not w3.is_connected():
        print("Error: Could not connect to Hardhat Node. Is it running?")
        return

    print("--- 🍓 FRESHCHAIN SENSOR SIMULATOR 🍓 ---")
    
    # Step A: Create a Batch
    print("\n1. Creating Batch #1: Strawberries ($1000)...")
    create_tx = contract.functions.createBatch("Strawberries", 1000)
    send_transaction(create_tx)
    print("✅ Batch Created on Blockchain.")
    
    time.sleep(2)

    # Step B: Report Good Temperature (20°C)
    print("\n2. Sensor Reading: 20°C (Safe)...")
    temp_tx_safe = contract.functions.updateTemperature(1, 20)
    receipt = send_transaction(temp_tx_safe)
    print("✅ Temperature Logged.")

    time.sleep(2)

    # Step C: Report Bad Temperature (35°C) -> Should Trigger Discount
    print("\n3. Sensor Reading: 35°C (DANGER!)...")
    temp_tx_danger = contract.functions.updateTemperature(1, 35)
    receipt = send_transaction(temp_tx_danger)
    
    # Check logs to see if price updated
    logs = contract.events.PriceUpdated().process_receipt(receipt)
    if logs:
        print(f"🚨 ALERT! Price Drop Detected on Chain!")
        print(f"   Batch ID: {logs[0]['args']['batchId']}")
        print(f"   New Price: ${logs[0]['args']['newPrice']} (Discounted from 1000)")
    else:
        print("✅ Temperature Logged.")

if __name__ == "__main__":
    main()