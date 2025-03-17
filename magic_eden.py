import asyncio
import random
from loguru import logger
import settings
import utils
from client import Client


class Magic:
    def __init__(self, client: Client):
        self.client = client
        self.nft_contract = self.client.w3.to_checksum_address(utils.get_nft_contract())
        self.mint_signature = f'0x9b4f3af5000000000000000000000000{self.client.account.address[2:]}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000'

    async def mint_nft(self):
        wait_time = random.randint(settings.TIME_AWAIT[0], settings.TIME_AWAIT[1])
        logger.info(
            f'Profile: {self.client.profile} Начну работу через {wait_time} секунд')
        await asyncio.sleep(wait_time)

        try:
            logger.info(
                f'Profile: {self.client.profile} {utils.get_account_address(self.client.private_key)} Mint NFT')
            tx = await self.client.send_transaction(
                to=self.nft_contract,
                data=self.mint_signature
            )

            if tx:
                try:
                    await self.client.verif_tx(tx_hash=tx)
                    logger.success(
                        f'Profile: {self.client.profile} {utils.get_account_address(self.client.private_key)} Transaction success!! tx_hash: 0x{tx.hex()}')
                except Exception as err:
                    logger.warning(
                        f'Profile: {self.client.profile} {utils.get_account_address(self.client.private_key)} Transaction error!! tx_hash: 0x{tx.hex()}; error: {err}')
                    raise ValueError(f'{self.client.profile} Ошибка транзакции')
            else:
                logger.error(
                    f'Profile: {self.client.profile} {utils.get_account_address(self.client.private_key)} Transaction error!!!')
                raise ValueError(f'{self.client.profile} Ошибка транзакции')
        except Exception as er:
            logger.error(
                f'Profile: {self.client.profile} {utils.get_account_address(self.client.private_key)} {er}')
