from thor_devkit import cry, transaction
import requests
from random import randint
import json

# Sender wallet information wird durch erstes Skript generiert
# mnemonic phrase: Muss noch von App importiert werden
# address: Muss noch von App importiert werden
# private key: Muss noch von App importiert werden. Aktuell zufällig erstelltes Wallet mit folgender adresse: 0x131de5b7f9052cd78526ceff3c74c9e909ee8d08
_privatekey = '***'
# Erstmal mit public Testnet Node
_node_url = 'https://testnet.veblocks.net'
# Gültig für Testnet, muss auf 74 geändert werden für Mainnet
_ChainTag = 39

# Get infos of best block
BlockInfos = requests.get(_node_url + '/blocks/best')	
# Set BlockRef to best block
_BlockRef = BlockInfos.json()['id'][0:18]
# Generate random noce
_Nonce = randint(10000000, 99999999)

# Hier noch input ändern falls bezahlt wurde
paid = 'true'

# Transaction with data will be send to this address: Aktuell unser Testnet TestWallet
address = '***'

# Hier wird der Sponsor der Transaktion angegeben: Aktuell unser Testnet TestWallet
sponsor = '***'

# ASCII <> Hex converter: hier müssen wir den Data Input noch anpassen

nachricht = '( ._.)/\(._. ) SayNode!'.encode('utf-8') # Ascii to binary

data = nachricht.hex() # Binary to Hex

_transaction_clauses = []
_transaction_clauses.append({'to': address, 'value': 0, 'data': '0x' + data})

### Build transaction 
body = {}
body['chainTag'] = _ChainTag
body['blockRef'] = _BlockRef
body['expiration'] = 720
body['clauses'] = _transaction_clauses
body['gasPriceCoef'] = 0
body['gas'] = 100000 # fixed to 100.000: Eventuell anpassen für grosse Transaktionen (Bilder etc.)
body['dependsOn'] = None
body['nonce'] = _Nonce
body['reserved'] = {"features": 1 }


# Hash und Private Key des Sponsors
sponsorurl = 'http://localhost:8000/'
headers = {'Content-type': 'application/json', 'Accept': '*/*'} 
sponsorhexhash = requests.post(sponsorurl, json = {'paid': paid, 'address': address, 'tx':body}, headers=headers)	
print(sponsorhexhash)

# Construct an unsigned transaction.
tx = transaction.Transaction(body)

# Sign the transaction with a private key.
priv_key = bytes.fromhex(_privatekey)
message_hash = tx.get_signing_hash()
signature = cry.secp256k1.sign(message_hash, priv_key)# + sponsorhexhash

# Set the signature on the transaction.
tx.set_signature(signature)

print('Created a transaction from ' + tx.get_origin() + ' with TXID: ' + tx.get_id() + '.')
print('')

encoded_bytes = tx.encode()

# Pretty print the encoded bytes.
print('The transaction will be send to the testnet node now.')

tx_headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
tx_data = {'raw': '0x' + encoded_bytes.hex()}
	
send_transaction = requests.post(_node_url + '/transactions', json=tx_data, headers=tx_headers)

print('Response from Server: ' + str(send_transaction.content))