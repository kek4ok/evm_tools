import config
import sys
from core.web3_utils import EVMWallet
from utils.logger import logger

menu_list = ["1. Create mnemonics",
             "2. Convert mnemonics to private keys",
             "3. Disperse money by keys",
             "4. Get balance",
             "5. Get ALL balances",
             "6. EXIT"]


def init_wallet():
    if config.MNEMONIC != '' or config.PRIVATE_KEY != '':
        try:
            wallet = EVMWallet(config.RPC, key=config.PRIVATE_KEY)
        except Exception:
            logger.error("Wallet init failed, fill config file correctly")
            raise "Bad_config"
    else:
        wallet = EVMWallet(config.RPC)
    return wallet


async def menu():
    def generate_mnemonics():
        count = int(input("Input mnemonics count: "))
        thrds = input("Input threads count (default 4): ")
        if thrds != '':
            wallet.generate_and_save_mnemonics(count, int(thrds))
        else:
            wallet.generate_and_save_mnemonics(count)

    async def disperse_by_keys():
        val_1 = float(input("Input lower range: "))
        val_2 = float(input("Input upper range: "))
        await wallet.disperse_money_by_keys((val_1, val_2))

    wallet = init_wallet()
    while 1:
        for _ in menu_list:
            print(_)
        inp = int(input("Choose option: "))
        match inp:
            case 1:
                generate_mnemonics()
            case 2:
                wallet.mnemonics_to_keys()
            case 3:
                await disperse_by_keys()
            case 4:
                logger.info(f"Curent balance: {await wallet.get_balance()}")
            case 5:
                await wallet.get_keys_balances()
            case 6:
                break
            case _:
                logger.error("Incorrect input!")
