import random
from eth_account import Account

def get_nft_contract():
    with open('nft_contracts.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = [i.strip() for i in lines]
        return random.choice(lines)


def get_account_address(private_key: str):
    account = Account.from_key(private_key)
    adress = account.address
    return adress