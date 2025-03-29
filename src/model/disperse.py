from web3 import Web3
import time
from typing import List

RPC_ENDPOINT = "https://carrot.megaeth.com/rpc"
CHAIN_ID = 6342

def get_balance(w3, account_address: str) -> int:
    return w3.eth.get_balance(account_address, 'latest')

def get_gas_params(w3) -> dict:
    try:
        gas_price = w3.eth.gas_price
        max_fee_per_gas = max(w3.to_wei(5, 'gwei'), int(gas_price * 1.5))
        max_priority_fee_per_gas = min(w3.to_wei(2, 'gwei'), max_fee_per_gas)
        print(f"Gas params: maxFeePerGas={w3.from_wei(max_fee_per_gas, 'gwei')} Gwei, "
              f"maxPriorityFeePerGas={w3.from_wei(max_priority_fee_per_gas, 'gwei')} Gwei")
        return {
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_priority_fee_per_gas
        }
    except Exception as e:
        print(f"Error fetching gas params: {e}")
        return {'gasPrice': w3.to_wei(5, 'gwei')}

def monitor_transaction(w3, tx_hash: str) -> bool:
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                print(f"Transaction {tx_hash} confirmed in block {receipt['blockNumber']}")
                return receipt['status'] == 1
        except:
            print(f"Waiting for transaction {tx_hash} to be confirmed...")
            time.sleep(0.5)
    print(f"Transaction {tx_hash} not confirmed after {max_attempts} attempts")
    return False

def disperse_funds(sender_private_key: str, recipient_keys: List[str], amount_per_wallet_eth: float) -> None:
    w3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
    if not w3.is_connected():
        raise Exception("Failed to connect to MegaETH testnet RPC")

    sender_account = w3.eth.account.from_key(sender_private_key)
    sender_address = sender_account.address
    print(f"\nDispersing funds from wallet: {sender_address}")

    balance = get_balance(w3, sender_address)
    print(f"Balance: {w3.from_wei(balance, 'ether')} ETH")
    if balance <= 0:
        print(f"No funds to disperse from {sender_address}")
        return

    amount_per_wallet_wei = w3.to_wei(amount_per_wallet_eth, 'ether')
    gas_params = get_gas_params(w3)
    gas_limit = 21000
    gas_cost_estimate = gas_params.get('maxFeePerGas', gas_params.get('gasPrice')) * gas_limit
    total_gas_cost = gas_cost_estimate * len(recipient_keys)
    total_amount_to_send = amount_per_wallet_wei * len(recipient_keys)
    total_required = total_amount_to_send + total_gas_cost

    if balance < total_required:
        print(f"Insufficient funds. Required: {w3.from_wei(total_required, 'ether')} ETH")
        return

    nonce = w3.eth.get_transaction_count(sender_address, 'pending')
    for recipient_key in recipient_keys:
        recipient_account = w3.eth.account.from_key(recipient_key)
        recipient_address = recipient_account.address
        print(f"\nSending to {recipient_address}: {amount_per_wallet_eth} ETH")

        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': amount_per_wallet_wei,
            'gas': gas_limit,
            'chainId': CHAIN_ID,
            **gas_params
        }

        try:
            signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)
            tx_hash = w3.to_hex(w3.eth.send_raw_transaction(signed_tx.raw_transaction))
            print(f"Tx Hash: {tx_hash}")
            if monitor_transaction(w3, tx_hash):
                print(f"Success: {amount_per_wallet_eth} ETH sent to {recipient_address}")
            else:
                print(f"Failed: Transaction to {recipient_address}")
        except Exception as e:
            print(f"Error: {str(e)}")

        nonce += 1
        time.sleep(0.5)
