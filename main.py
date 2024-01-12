import asyncio

from utils.utils import menu


async def main():
    await menu()


if __name__ == '__main__':
    asyncio.run(main())
