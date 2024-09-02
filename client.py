import asyncio
import random

from logger import logger
from settings import (
    NUM_CLIENTS, SERVER_HOST, SERVER_PORT, COUNT_MESSAGES,
    DELAY_BEFORE_SEND, DELAY_AFTER_SEND
)


async def send_messages(reader, writer, client_id, response_messages=0):
    """
    Отправляет сообщения от клиента серверу.
    """
    for msg_num in range(1, COUNT_MESSAGES+1):
        await asyncio.sleep(random.uniform(DELAY_BEFORE_SEND, DELAY_AFTER_SEND))
        message = f'Hello from client {client_id}, message {msg_num}'
        logger.info(f'Отправлено сообщение клиентом {client_id}: {message}')
        writer.write(message.encode())
        await writer.drain()
        response_messages += 1

        if response_messages == COUNT_MESSAGES:
            writer.close()


async def start_clients(server):
    """
    Запускает клиентов. Ожидает завершения отправки всех сообщений клиентами и
    останавливает их работу.
    """
    tasks = []
    try:
        for client_id in range(1, NUM_CLIENTS+1):
            reader, writer = await asyncio.open_connection(
                SERVER_HOST, SERVER_PORT
            )
            task = asyncio.create_task(send_messages(reader, writer, client_id))
            tasks.append(task)

        await asyncio.gather(*tasks)

        server.close()
        await server.wait_closed()

    except Exception as e:
        logger.error(e)
