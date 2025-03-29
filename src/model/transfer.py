from web3 import Web3
import time

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

def transfer_funds(private_key: str, to_address: str) -> None:
    w3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
    if not w3.is_connected():
        raise Exception("Failed to connect to MegaETH testnet RPC")

    account = w3.eth.account.from_key(private_key)
    from_address = account.address
    print(f"\nProcessing wallet: {from_address}")

    balance = get_balance(w3, from_address)
    print(f"Balance: {w3.from_wei(balance, 'ether')} ETH")
    if balance <= 0:
        print(f"No funds to transfer")
        return

    gas_params = get_gas_params(w3)
    gas_limit = 21000
    gas_cost_estimate = gas_params.get('maxFeePerGas', gas_params.get('gasPrice')) * gas_limit
    buffer = w3.to_wei(1, 'gwei')
    total_cost = gas_cost_estimate + buffer

    if balance <= total_cost:
        print(f"Insufficient funds for gas + buffer")
        return

    amount_to_send = balance - total_cost
    print(f"Amount to send: {w3.from_wei(amount_to_send, 'ether')} ETH")

    nonce = w3.eth.get_transaction_count(from_address, 'pending')
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': amount_to_send,
        'gas': gas_limit,
        'chainId': CHAIN_ID,
        **gas_params
    }

    try:
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.to_hex(w3.eth.send_raw_transaction(signed_tx.raw_transaction))
        print(f"Tx Hash: {tx_hash}")
        if monitor_transaction(w3, tx_hash):
            print(f"Success: Funds transferred from {from_address}")
        else:
            print(f"Failed: Transaction from {from_address}")
    except Exception as e:
        print(f"Error: {str(e)}")
