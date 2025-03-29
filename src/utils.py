from web3 import Web3
import time

def connect_to_web3(rpc_endpoint: str) -> Web3:
    """Connect to the MegaETH testnet."""
    w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
    if not w3.is_connected():
        raise Exception("Failed to connect to MegaETH testnet RPC")
    return w3

def get_balance(w3: Web3, account_address: str) -> int:
    """Get the balance of an account using eth_getBalance."""
    balance = w3.eth.get_balance(account_address, 'latest')
    return balance

def get_gas_params(w3: Web3) -> dict:
    """Fetch dynamic gas parameters with proper EIP-1559 values."""
    try:
        gas_price = w3.eth.gas_price  # Base fee from network
        max_fee_per_gas = max(w3.to_wei(5, 'gwei'), int(gas_price * 1.5))  # Minimum 5 Gwei
        max_priority_fee_per_gas = min(w3.to_wei(2, 'gwei'), max_fee_per_gas)  # Max 2 Gwei, but ≤ maxFeePerGas
        print(f"Gas params: maxFeePerGas={w3.from_wei(max_fee_per_gas, 'gwei')} Gwei, "
              f"maxPriorityFeePerGas={w3.from_wei(max_priority_fee_per_gas, 'gwei')} Gwei")
        return {
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_priority_fee_per_gas
        }
    except Exception as e:
        print(f"Error fetching gas params: {e}")
        return {'gasPrice': w3.to_wei(5, 'gwei')}  # Fallback to 5 Gwei

def monitor_transaction(w3: Web3, tx_hash: str) -> bool:
    """Monitor the transaction receipt."""
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                print(f"Transaction {tx_hash} confirmed in block {receipt['blockNumber']}")
                return receipt['status'] == 1  # True if successful
        except:
            print(f"Waiting for transaction {tx_hash} to be confirmed...")
            time.sleep(0.5)  # Poll every 0.5 seconds
    print(f"Transaction {tx_hash} not confirmed after {max_attempts} attempts")
    return False
