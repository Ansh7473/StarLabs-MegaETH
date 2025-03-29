from web3 import Web3
import time
from src.utils.web3_utils import connect_to_web3, get_balance, get_gas_params, monitor_transaction

RPC_ENDPOINT = "https://carrot.megaeth.com/rpc"  # MegaETH testnet RPC
CHAIN_ID = 6342  # MegaETH testnet chain ID

def transfer_funds(w3: Web3, private_key: str, to_address: str) -> None:
    """Transfer all funds from a wallet to the main wallet, leaving gas cost plus a tiny buffer."""
    account = w3.eth.account.from_key(private_key)
    from_address = account.address

    # Get the current balance
    balance = get_balance(w3, from_address)
    print(f"Balance of {from_address}: {balance} Wei ({w3.from_wei(balance, 'ether')} ETH)")

    if balance <= 0:
        print(f"No funds to transfer from {from_address}")
        return

    # Get gas parameters
    gas_params = get_gas_params(w3)
    gas_limit = 21000  # Standard gas limit for a simple transfer

    # Estimate gas cost
    gas_cost_estimate = gas_params.get('maxFeePerGas', gas_params.get('gasPrice')) * gas_limit
    print(f"Estimated gas cost: {gas_cost_estimate} Wei ({w3.from_wei(gas_cost_estimate, 'ether')} ETH)")

    # Add a tiny buffer (1 Gwei worth) to avoid edge-case rejection
    buffer = w3.to_wei(1, 'gwei')  # 0.000001 ETH
    total_cost = gas_cost_estimate + buffer

    # Check if balance is sufficient for gas + buffer
    if balance <= total_cost:
        print(f"Insufficient funds for gas + buffer in {from_address}. Required: {w3.from_wei(total_cost, 'ether')} ETH")
        return

    # Calculate amount to send (all funds minus gas cost and buffer)
    amount_to_send = balance - total_cost
    # No minimum amount check - allow even 1 Wei to be sent

    print(f"Amount to send: {amount_to_send} Wei ({w3.from_wei(amount_to_send, 'ether')} ETH)")

    # Build the transaction
    nonce = w3.eth.get_transaction_count(from_address, 'pending')
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': amount_to_send,
        'gas': gas_limit,
        'chainId': CHAIN_ID,
        **gas_params
    }

    # Sign and send the transaction
    try:
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = w3.to_hex(tx_hash)
        print(f"Transaction sent from {from_address} to {to_address}. Tx Hash: {tx_hash_hex}")
        
        # Monitor transaction
        success = monitor_transaction(w3, tx_hash_hex)
        if success:
            print(f"Successfully transferred funds from {from_address}")
        else:
            print(f"Transaction from {from_address} failed")
    except Exception as e:
        print(f"Error sending transaction from {from_address}: {str(e)}")

def run_transfer():
    """Run the transfer process."""
    w3 = connect_to_web3(RPC_ENDPOINT)
    with open('data/target_address.txt', 'r') as f:
        target_address = f.read().strip()
    with open('data/private_keys.txt', 'r') as f:
        source_wallets = [line.strip() for line in f.readlines() if line.strip()]

    print("Running Transfer Mode: private_keys.txt to target_address.txt")
    for private_key in source_wallets:
        account = w3.eth.account.from_key(private_key)
        print(f"\nProcessing wallet: {account.address}")
        transfer_funds(w3, private_key, target_address)
        time.sleep(0.5)  # Delay between wallets
