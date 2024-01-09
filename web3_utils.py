import random

from eth_account import Account
from eth_account.messages import encode_defunct, SignableMessage, encode_structured_data
from web3.eth import AsyncEth
from web3 import Web3
import concurrent.futures
from rpcs import rpc_list, chain_id_list


class EVMWallet:
    def __init__(self, provider: str = None, mnemonic: str = None, key: str = None):
        self.chain_id = chain_id_list.get(provider)
        self.w3 = None
        Account.enable_unaudited_hdwallet_features()
        if mnemonic:
            self.mnemonic = mnemonic
            self.account = Account.from_mnemonic(mnemonic)
        elif key:
            self.mnemonic = ""
            self.account = Account.from_key(key)

        self.accounts = []
        self.keys = []
        self.define_new_provider(rpc_list.get(provider))

    def define_new_provider(self, http_provider: str):
        self.w3 = Web3(Web3.AsyncHTTPProvider(http_provider), modules={'eth': (AsyncEth,)}, middlewares=[])

    def create_wallet(self):
        self.account, self.mnemonic = Account.create_with_mnemonic()
        return self.account, self.mnemonic

    def get_key_from_mnemonic(self, mnemonic, path=None):
        if path:
            account = self.w3.eth.account.from_mnemonic(mnemonic, account_path=path)
        else:
            account = self.w3.eth.account.from_mnemonic(mnemonic)
        return account.key.hex()

    async def get_balance(self):
        balance = await self.w3.eth.get_balance(self.account.address)
        return self.w3.from_wei(balance, 'ether')

    def sign(self, encoded_msg: SignableMessage):
        return self.w3.eth.account.sign_message(encoded_msg, self.account.key)

    def get_signed_code(self, msg) -> str:
        return self.sign(encode_defunct(text=msg)).signature.hex()

    def get_signed_code_struct(self, msg) -> str:
        return self.sign(encode_structured_data(msg)).signature.hex()

    def generate_and_save_mnemonics(self, num_wallets: int, num_threads: int = 4, filename: str = 'mnemonics.txt'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(self.create_wallet) for _ in range(num_wallets)]

            for future in concurrent.futures.as_completed(futures):
                account, mnemonic = future.result()
                self.accounts.append((account, mnemonic))

            self._save_mnemonics_to_file(filename)

    def _save_mnemonics_to_file(self, filename: str):
        with open(filename, 'w') as file:
            for account, mnemonic in self.accounts:
                file.write(f"{mnemonic}\n")

    def _save_keys_to_file(self, filename: str):
        with open(filename, 'w') as file:
            for key in self.keys:
                file.write(f"{key}\n")

    def mnemonics_to_keys(self, mnemonics_file="mnemonics.txt", filename: str = "keys.txt"):
        with open(mnemonics_file, 'r') as f:
            mnemonics = [mnem.replace('\n', '') for mnem in f.readlines()]
        self.keys = [self.get_key_from_mnemonic(mnem) for mnem in mnemonics]
        self._save_keys_to_file(filename)

    async def disperse_money_by_keys(self, val_range):
        with open('keys.txt', 'r') as f:
            keys = [mnem.replace('\n', '') for mnem in f.readlines()]
        nonce = await self.w3.eth.get_transaction_count(self.account.address)
        for key in keys:
            value = random.uniform(*val_range)
            if keys.index(key) == 0:
                nonce = nonce
            else:
                nonce += 1
            await self.send_money_to(Account.from_key(key).address, value, nonce)
        print("SUCCESS")

    async def send_money_to(self, address: str, value: float, nonce: int = None):
        if nonce is None:
            nonce = await self.w3.eth.get_transaction_count(self.account.address)
        estimate = await self.w3.eth.estimate_gas({
            'to': address,
            'from': self.account.address,
            'value': self.w3.to_wei(value, 'ether')})
        tx = {
            'nonce': nonce,
            'to': address,
            'value': self.w3.to_wei(value, 'ether'),
            'gas': estimate,
            'gasPrice': await self.w3.eth.gas_price,
            'chainId': self.chain_id
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key.hex())
        tx_hash = await self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(address)
        print(self.w3.to_hex(tx_hash))
