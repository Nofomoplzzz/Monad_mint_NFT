import asyncio
import settings
from client import Client
from magic_eden import Magic
import csv


async def process_row(private_key, proxy, semaphore, profile):
    await semaphore.acquire()
    magic = Magic(
        Client(
            private_key=private_key,
            rpc='https://testnet-rpc.monad.xyz',
            proxy=proxy,
            profile=profile
        )
    )

    await magic.mint_nft()
    await magic.client.w3.provider.disconnect()
    semaphore.release()


async def main():
    max_concurrent_tasks = settings.THREADS
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    tasks = []
    with open('profiles.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            private_key = row['Private_Key']
            proxy = row['Proxy']
            profile = row['Profile']

            tasks.append(process_row(private_key, proxy, semaphore, profile))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
