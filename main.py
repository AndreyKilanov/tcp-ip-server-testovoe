import asyncio

from server import start_server_and_clients


async def main():
    server_task = asyncio.create_task(start_server_and_clients())
    await asyncio.gather(server_task)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
