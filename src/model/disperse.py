from web3 import Web3
import time
from src.utils.web3_utils import connect_to_web3, get_balance, get_gas_params, monitor_transaction

RPC_ENDPOINT = "https://carrot.megaeth.com/rpc"  # MegaETH testnet RPC
CHAIN_ID = 6342  # MegaETH testnet chain ID

def disperse_funds(w3: Web3, sender_private_key: str, recipient_private_keys: list) -> None:
    """Disperse a user-chosen amount from one wallet to all recipient wallets."""
    sender_account = w3.eth.account.from_key(sender_private_key)
    sender_address = sender_account.address
    print(f"\nDispersing funds from wallet: {sender_address}")

    # Get sender balance
    balance = get_balance(w3, sender_address)
    print(f"Balance of {sender_address}: {balance} Wei ({w3.from_wei(balance, 'ether')} ETH)")

    if balance <= 0:
        print(f"No funds to disperse from {sender_address}")
        return

    # Get user input for amount to send to each wallet (in ETH)
    try:
        amount_per_wallet_eth = float(input("Enter amount to send to each wallet (in ETH): "))
        amount_per_wallet_wei = w3.to_wei(amount_per_wallet_eth, 'ether')
    except ValueError:
        print("Invalid input: Please enter a valid number")
        return

    # Calculate total cost (amount per wallet * number of recipients + gas costs)
    gas_params = get_gas_params(w3)
    gas_limit = 21000
    gas_cost_estimate = gas_params.get('maxFeePerGas', gas_params.get('gasPrice')) * gas_limit
    total_gas_cost = gas_cost_estimate * len(recipient_private_keys)
    total_amount_to_send = amount_per_wallet_wei * len(recipient_private_keys)
    total_required = total_amount_to_send + total_gas_cost

    if balance < total_required:
        print(f"Insufficient funds in {sender_address}. Required: {w3.from_wei(total_required, 'ether')} ETH")
        return

    # Disperse funds to each wallet
    nonce = w3.eth.get_transaction_count(sender_address, 'pending')
    for recipient_private_key in recipient_private_keys:
        recipient_account = w3.eth.account.from_key(recipient_private_key)
        recipient_address = recipient_account.address

        print(f"\nSending to {recipient_address}")
        print(f"Amount to send: {amount_per_wallet_wei} Wei ({w3.from_wei(amount_per_wallet_wei, 'ether')} ETH)")

        # Build the transaction
        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': amount_per_wallet_wei,
            'gas': gas_limit,
            'chainId': CHAIN_ID,
            **gas_params
        }

        # Sign and send
        try:
            signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash_hex = w3.to_hex(tx_hash)
            print(f"Transaction sent from {sender_address} to {recipient_address}. Tx Hash: {tx_hash_hex}")

            # Monitor transaction
            success = monitor_transaction(w3, tx_hash_hex)
            if success:
                print(f"Successfully sent {w3.from_wei(amount_per_wallet_wei, 'ether')} ETH to {recipient_address}")
            else:
                print(f"Transaction to {recipient_address} failed")
        except Exception as e:
            print(f"Error sending transaction to {recipient_address}: {str(e)}")

        nonce += 1  # Increment nonce for the next transaction
        time.sleep(0.5)  # Delay between transactions

def run_disperse():
    """Run the disperse process."""
    w3 = connect_to_web3(RPC_ENDPOINT)
    with open('data/wallet.txt', 'r') as f:
        sender_private_key = f.read().strip()
    with open('data/recipient_wallets.txt', 'r') as f:
        recipient_wallets = [line.strip() for line in f.readlines() if line.strip()]

    print("Running Disperse Mode: wallet.txt to recipient_wallets.txt")
    disperse_funds(w3, sender_private_key, recipient_wallets)
