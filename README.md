# evm_tools
## Requirements
`Python  3.10 or higher`

## Instalation
```pip install -r .\requirements.txt```

## Run
```python main.py```

## Config

`PRIVATE_KEY` - Private key from your wallet

`RPC`  - Network that will be used for provider. You can add new in `utils/rpcs.py`.
USE ONLY THE NAME (example 'opBNB')

`MNEMONIC` - Your mnemonic phrase | OPTIONAL

## Functions
### Create mnemonics
Creates the specified number of mnemonic phrases and saves them to a file mnemonics.txt
### Convert mnemonics to private keys
Converts mnemonic phrases from a file mnemonics.txt to private keys and save into keys.txt
### Disperse money by keys
Sends the specified range of money from an authorized wallet to all addresses using the private key from the file keys.txt
### Get balance
Returns the balance of the authorized wallet
### Get ALL balances
Retrieves all balances for addresses from private keys

