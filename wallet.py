import subprocess
import json
import os
from dotenv import load_dotenv 
from constants import *
from bit import Key, PrivateKey, PrivateKeytTestnet
from bit.network import NetworkAPI
from bit import *
from web3 import Web3
from eth_account import Account 

load_dotenv()

command = './derive -g --mnemonic="father left twin fine chicken okay girl vapor scissors involve mushroom tip" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)


def create_trx(coin, account, recipient, amount):
    """create the raw, unsigned transaction that contains all metadata needed to transact"""
    global trx_data
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        trx_data = {
            "chainId" : 100,
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
        return trx_data

    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
    

    
# create a function to hold Ethereum 
eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH,5)[0]['privkey'])



# create a function to send trx
def send_trx(coin,account,recipient, amount):
    txn = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)

