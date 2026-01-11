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
# Matches FreshChain.sol
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_batchId", "type": "string"},
            {"internalType": "string", "name": "_productType", "type": "string"}
        ],
        "name": "createBatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_batchId", "type": "string"},
            {"internalType": "string", "name": "_status", "type": "string"},
            {"internalType": "string", "name": "_location", "type": "string"}
        ],
        "name": "updateLocation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_batchId", "type": "string"},
            {"internalType": "string", "name": "_alertType", "type": "string"},
            {"internalType": "bytes", "name": "_encryptedSensorData", "type": "bytes"}
        ],
        "name": "reportExcursion",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_batchId", "type": "string"}
        ],
        "name": "getBatchDetails",
        "outputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "string", "name": "productType", "type": "string"},
            {
                "components": [
                    {"internalType": "string", "name": "status", "type": "string"},
                    {"internalType": "string", "name": "location", "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
                ],
                "internalType": "struct FreshChain.TrackingEvent[]",
                "name": "history",
                "type": "tuple[]"
            },
            {
                "components": [
                    {"internalType": "string", "name": "alertType", "type": "string"},
                    {"internalType": "bytes", "name": "encryptedData", "type": "bytes"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
                ],
                "internalType": "struct FreshChain.SensorAlert[]",
                "name": "alerts",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
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

    print("--- FRESHCHAIN SENSOR SIMULATOR ---")

    batch_id = "batch-001"
    product = "Strawberries"

    print(f"\n1. Creating batch '{batch_id}' for {product}...")
    create_tx = contract.functions.createBatch(batch_id, product)
    send_transaction(create_tx)
    print("✅ Batch created.")

    time.sleep(1)

    print("\n2. Updating location: In Transit @ NH45, Chennai...")
    location_tx = contract.functions.updateLocation(batch_id, "In Transit", "NH45, Chennai")
    send_transaction(location_tx)
    print("✅ Location updated.")

    time.sleep(1)

    print("\n3. Reporting temperature excursion (TEMP_HIGH, 35C)...")
    alert_payload = "TEMP:35C".encode()
    alert_tx = contract.functions.reportExcursion(batch_id, "TEMP_HIGH", alert_payload)
    send_transaction(alert_tx)
    print("✅ Excursion reported.")

    time.sleep(1)

    print("\n4. Fetching batch details...")
    batch_details = contract.functions.getBatchDetails(batch_id).call()

    batch_id_on_chain, product_type, history, alerts = batch_details
    print(f"Batch ID: {batch_id_on_chain}")
    print(f"Product: {product_type}")
    print("History events:")
    for evt in history:
        status, location, ts = evt
        print(f" - {status} @ {location} (ts: {ts})")

    print("Alerts:")
    for alert in alerts:
        alert_type, encrypted, ts = alert
        print(f" - {alert_type} payload={encrypted.hex()} (ts: {ts})")

if __name__ == "__main__":
    main()